import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def classify(model_name, text, max_new_tokens):
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    prompt = f"Task: Classify the stock headline into Positive, Neutral, or Negative and give a one-line rationale.\nHeadline: {text}\nAnswer format: <Label> | <Rationale>\nAnswer:"
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    txt = tok.decode(out[0], skip_special_tokens=True)
    ans = txt.split("Answer:")[-1].strip()
    return ans

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    p.add_argument("--text", required=True)
    p.add_argument("--max_new_tokens", type=int, default=64)
    args = p.parse_args()
    torch.set_grad_enabled(False)
    res = classify(args.model, args.text, args.max_new_tokens)
    print(res)
