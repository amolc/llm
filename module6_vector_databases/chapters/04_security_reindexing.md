# Chapter 6.4: Data Security, PII Masking, Re-indexing

Building a production-ready Vector DB system requires more than just storing vectors. You must also protect the data and ensure it stays up-to-date.

---

## **1. Data Security & PII Masking**

When you build a vector index of user data, the vector itself is a representation of that data. If the index is compromised, sensitive information can be reconstructed (Vector Reconstruction Attack).

### **A. PII (Personally Identifiable Information) Masking**
Before you create an embedding, you must mask or redact PII:
- **Masking**: Replace "Amol C" with "[USER_NAME]".
- **Redaction**: Replace sensitive fields with "[REDACTED]".

### **B. Input/Output Filtering**
Use specialized models (e.g., Presidio) or LLM guardrails (e.g., NeMo Guardrails) to filter PII from queries and retrieved chunks.

---

## **2. Re-indexing & Vector Drift**

Vector indices are not static. They must be maintained.

### **A. Re-indexing Strategies**
When do you need to re-index?
1.  **New Embedding Model**: If you upgrade from `text-embedding-ada-002` to `text-embedding-3-small`, you must re-embed all documents.
2.  **Stale Data**: When document content is updated, the corresponding vector in the DB must be replaced.

### **B. Vector Drift**
Over time, as new data is added, the structure of your vector space can change. Periodic re-indexing of the entire dataset can improve search accuracy.

---

## **3. Sample Code: Basic PII Masking with Regex**

```python
import re

def mask_pii(text):
    # 1. Mask Email Addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    masked_text = re.sub(email_pattern, "[EMAIL_REDACTED]", text)
    
    # 2. Mask Phone Numbers (Simple US-style)
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    masked_text = re.sub(phone_pattern, "[PHONE_REDACTED]", masked_text)
    
    return masked_text

raw_text = "Contact amol@example.com at (555) 123-4567 for more details."
print(f"Raw: {raw_text}")
print(f"Masked: {mask_pii(raw_text)}")
```

---

## **Recommended Reading**
1.  **[Microsoft Presidio: Data Protection & PII Recognition](https://github.com/microsoft/presidio)**
2.  **[NVIDIA NeMo Guardrails: PII Filtering](https://github.com/NVIDIA/NeMo-Guardrails/blob/main/docs/user_guides/pii_masking.md)**
3.  **[Vector Database Security (Cloud Security Alliance)](https://cloudsecurityalliance.org/)**
