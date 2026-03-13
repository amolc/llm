import asyncio
import random
import os
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="/Users/amolc/2026/llm/.env")

LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Define paths relative to the script location for visibility
BASE_DIR = "/Users/amolc/2026/llm/linkedinresearch"
SESSION_FILE = os.path.join(BASE_DIR, "linkedin_session.json")
OUTPUT_CSV = os.path.join(BASE_DIR, "linkedin_leads.csv")

class LinkedInBot:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.leads = []

    async def start(self, headless=False):
        """Initialize the browser and context."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        
        # Load session if it exists
        if os.path.exists(SESSION_FILE):
            print(f"Loading session from {SESSION_FILE}...")
            try:
                with open(SESSION_FILE, 'r') as f:
                    storage_state = json.load(f)
                self.context = await self.browser.new_context(storage_state=storage_state)
            except Exception as e:
                print(f"Error loading session: {e}. Starting new context.")
                self.context = await self.browser.new_context()
        else:
            print(f"No session found at {SESSION_FILE}. Starting a new context.")
            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()
        # Apply stealth using the Stealth class
        await Stealth().apply_stealth_async(self.page)

    async def login(self):
        """Handle login if needed."""
        if not self.page:
            raise RuntimeError("Bot not started. Call start() first.")

        await self.page.goto("https://www.linkedin.com/login")
        await asyncio.sleep(random.uniform(2, 4))
        
        # Check if already logged in
        if "feed" in self.page.url or await self.page.query_selector(".global-nav__me"):
            print("Already logged in.")
            return

        if LINKEDIN_USERNAME and LINKEDIN_PASSWORD:
            print(f"Attempting automatic login for {LINKEDIN_USERNAME}...")
            await self.page.fill("#username", LINKEDIN_USERNAME)
            await asyncio.sleep(random.uniform(1, 2))
            await self.page.fill("#password", LINKEDIN_PASSWORD)
            await asyncio.sleep(random.uniform(1, 2))
            await self.page.click('button[type="submit"]')
            
            # Check for 2FA or successful login
            try:
                await self.page.wait_for_url("**/feed/**", timeout=20000)
                print("Login successful.")
            except Exception:
                print("Login might require manual intervention (2FA, etc.).")
        else:
            print("Credentials not found in .env. Please log in manually in the opened browser window.")
            # Wait for user to log in manually (timeout 5 minutes)
            try:
                await self.page.wait_for_url("**/feed/**", timeout=300000)
                print("Manual login successful.")
            except Exception:
                print("Login timed out.")
                return

        # Save session after successful login
        if self.context:
            storage = await self.context.storage_state()
            os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
            with open(SESSION_FILE, 'w') as f:
                json.dump(storage, f)
            print(f"Session saved to {SESSION_FILE}")

    async def search_and_message(self, keywords, message_template):
        """Search for people, collect names, and send an intro message."""
        if not self.page:
            raise RuntimeError("Bot not started. Call start() first.")

        # Broader search URL (people results)
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={keywords}"
        print(f"Searching for: {keywords}")
        await self.page.goto(search_url)
        
        # Initial wait for page structure
        await asyncio.sleep(random.uniform(7, 10))

        # Forced scrolling to trigger lazy-loading of search results
        print("Scrolling to load results...")
        for _ in range(5):
            await self.page.evaluate("window.scrollBy(0, 400)")
            await asyncio.sleep(1.5)

        # Re-check for results using multiple selector types
        print("Scanning for result containers...")
        # Add broad container selectors
        containers = await self.page.query_selector_all(".reusable-search__result-container, li.search-result, .search-results-container li, [data-chameleon-result-urn], .entity-result")
        
        if not containers:
            print("Broad containers not found. Trying deeper scan for action buttons...")
            # Scan for ANY action button that implies a result row
            action_buttons = await self.page.query_selector_all('button:has-text("Connect"), button:has-text("Message"), button:has-text("Follow")')
            
            if action_buttons:
                print(f"Found {len(action_buttons)} action buttons directly.")
                processed_count = 0
                for i, button in enumerate(action_buttons):
                    if processed_count >= 5: break # Limit fallbacks
                    
                    try:
                        text = (await button.inner_text()).strip()
                        if "Connect" not in text: continue
                        
                        # Find the name nearby (usually in a heading or span above the button)
                        parent_handle = await button.evaluate_handle("el => el.closest('li, div.entity-result, .search-result')")
                        parent = parent_handle.as_element()
                        if parent:
                            name_elem = await parent.query_selector(".entity-result__title-text a span[aria-hidden='true'], .actor-name, h3, .t-16")
                            name = (await name_elem.inner_text()).strip() if name_elem else f"Contact {i+1}"
                            
                            headline_elem = await parent.query_selector(".entity-result__primary-subtitle, .subline-level-1, .t-14")
                            headline = (await headline_elem.inner_text()).strip() if headline_elem else "No headline"
                            
                            print(f"\n[{i+1}] Found via direct button: {name}")
                            await self.process_connection(button, name, message_template, headline)
                            processed_count += 1
                    except Exception as e:
                        print(f"Error processing direct button {i+1}: {e}")
                return

        if not containers:
            print("STILL NO RESULTS FOUND. The page might be protected or the search term returned nothing.")
            print("Try checking the browser window to see if results are visible.")
            return

        print(f"Total results identified: {len(containers)}")

        for i, container in enumerate(containers[:10]): # Process top 10 results
            try:
                # Extract Name - try multiple possible patterns
                name = "Unknown"
                name_selectors = [
                    ".entity-result__title-text a span[aria-hidden='true']",
                    ".actor-name",
                    ".name.actor-name",
                    "span.t-roman"
                ]
                for ns in name_selectors:
                    name_elem = await container.query_selector(ns)
                    if name_elem:
                        name = (await name_elem.inner_text()).strip()
                        break
                
                # Extract Headline
                headline = "No headline"
                headline_selectors = [
                    ".entity-result__primary-subtitle",
                    ".subline-level-1",
                    ".headline",
                    ".t-14.t-black--light"
                ]
                for hs in headline_selectors:
                    headline_elem = await container.query_selector(hs)
                    if headline_elem:
                        headline = (await headline_elem.inner_text()).strip()
                        break
                
                print(f"\n[{i+1}] Processing: {name}")
                print(f"    Headline: {headline}")

                # Find the action button (Connect/Message/Follow)
                button = await container.query_selector('button:has-text("Connect")')
                
                if button:
                    await self.process_connection(button, name, message_template, headline)
                else:
                    # Check if already connected (Message button instead)
                    msg_button = await container.query_selector('button:has-text("Message")')
                    status = "Already Connected" if msg_button else "Not Connectable"
                    print(f"    Status: {status}")
                    self.leads.append({
                        "Name": name,
                        "Headline": headline,
                        "Status": status,
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    self.save_to_csv()

                # Human-like pause between contacts
                await asyncio.sleep(random.uniform(12, 18))

            except Exception as e:
                print(f"    Error processing contact {i+1}: {e}")

    async def process_connection(self, button, name, message_template, headline="No headline"):
        """Handles the actual connection request logic."""
        if not self.page:
            print(f"    Error: Page object is None for {name}")
            return

        status = "Failed"
        try:
            # Scroll button into view before clicking
            await button.scroll_into_view_if_needed()
            await asyncio.sleep(random.uniform(2, 3))
            
            print(f"    Clicking 'Connect' for {name}...")
            await button.click()
            await asyncio.sleep(random.uniform(3, 5))

            # Check for "Add a note" button
            add_note_button = await self.page.query_selector('button:has-text("Add a note")')
            if add_note_button:
                await add_note_button.click()
                await asyncio.sleep(random.uniform(2, 4))
                
                # Personalize message with name if possible
                first_name = name.split()[0] if " " in name else name
                personalized_message = message_template.replace("[Name]", first_name)
                
                # Fill the message
                print(f"    Typing message for {name}...")
                await self.page.fill("textarea", personalized_message)
                await asyncio.sleep(random.uniform(3, 6))
                
                # Click Send
                send_button = await self.page.query_selector('button:has-text("Send")')
                if send_button:
                    print(f"    Sending connection request to {name}...")
                    await send_button.click()
                    status = "Connection Sent"
                else:
                    print(f"    Could not find 'Send' button for {name}")
                    status = "Send Button Not Found"
            else:
                # Check for a "Send now" or similar direct connect
                send_now = await self.page.query_selector('button:has-text("Send now")')
                if send_now:
                    print(f"    Sending direct connection (no note allowed) to {name}...")
                    await send_now.click()
                    status = "Sent Directly"
                else:
                    print(f"    No 'Add a note' option for {name}. Checking if note limit reached or profile restricted.")
                    status = "No Note Option/Restricted"

            # Close any open modal (like success confirmations)
            dismiss_button = await self.page.query_selector('button[aria-label="Dismiss"]')
            if dismiss_button:
                await dismiss_button.click()
                await asyncio.sleep(1)

        except Exception as e:
            print(f"    Error in process_connection for {name}: {e}")
            status = f"Error: {str(e)[:50]}"

        # Store lead info
        self.leads.append({
            "Name": name,
            "Headline": headline,
            "Status": status,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_to_csv()

    def save_to_csv(self):
        """Save collected leads to a CSV file."""
        if not self.leads:
            return

        file_exists = os.path.isfile(OUTPUT_CSV)
        keys = self.leads[0].keys()

        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        with open(OUTPUT_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            if not file_exists:
                writer.writeheader()
            # Only write the last lead added to avoid duplicates since we call this in a loop
            writer.writerow(self.leads[-1])
        
        print(f"    Data for '{self.leads[-1]['Name']}' saved to {OUTPUT_CSV}")

    async def close(self):
        """Clean up resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

async def main():
    bot = LinkedInBot()
    # Run in headed mode to allow manual login/review
    await bot.start(headless=False)
    
    try:
        await bot.login()
        
        # Prop Trader specific keywords and message
        keywords = '("Prop Trader" OR "Funded Trader") AND ("FTMO" OR "Topstep" OR "Apex")'
        # Template uses [Name] for personalization
        message = "Hi [Name], I saw you're trading with top prop firms. I've built an intelligence layer that helps funded traders avoid 'accidental' drawdown breaches through automated risk monitoring. Would love to connect and show you how it works!"
        
        await bot.search_and_message(keywords, message)
        
        print("\nBot finished its task. Keeping browser open for 30 seconds for review...")
        await asyncio.sleep(30)
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
