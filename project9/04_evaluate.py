import argparse, json
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

def load_jsonl(p):
    return [json.loads(l) for l in open(p, "r", encoding="utf-8").read().splitlines() if l.strip()]

def infer(model, tok, inp, max_new_tokens):
    prompt = f"Task: Classify the stock headline into Positive, Neutral, or Negative and give a one-line rationale.\nHeadline: {inp}\nAnswer format: <Label> | <Rationale>\nAnswer:"
    x = tok(prompt, return_tensors="pt").to(model.device)
    y = model.generate(**x, max_new_tokens=max_new_tokens, do_sample=False)
    t = tok.decode(y[0], skip_special_tokens=True).split("Answer:")[-1].strip()
    return t

def load_base(model_name):
    tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    m = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
    return m, tok

def load_lora(base, adapter_dir):
    m, t = load_base(base)
    m = PeftModel.from_pretrained(m, adapter_dir)
    return m, t

def accuracy(pred, gold):
    a = pred.split("|")[0].strip().lower()
    b = gold.strip().lower()
    return 1 if a == b else 0

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--eval_jsonl", default="data/sample_eval.jsonl")
    p.add_argument("--baseline_model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    p.add_argument("--lora_dir", default=None)
    p.add_argument("--qlora_dir", default=None)
    p.add_argument("--base_for_adapters", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    p.add_argument("--max_new_tokens", type=int, default=64)
    args = p.parse_args()
    torch.set_grad_enabled(False)

    data = load_jsonl(args.eval_jsonl)

    m_b, t_b = load_base(args.baseline_model)
    s, n = 0, 0
    for r in data:
        y = infer(m_b, t_b, r["input"], args.max_new_tokens)
        s += accuracy(y, r["output"])
        n += 1
    print(f"baseline_acc={s/n:.2f}")

    if args.lora_dir:
        m_l, t_l = load_lora(args.base_for_adapters, args.lora_dir)
        s, n = 0, 0
        for r in data:
            y = infer(m_l, t_l, r["input"], args.max_new_tokens)
            s += accuracy(y, r["output"])
            n += 1
        print(f"lora_acc={s/n:.2f}")

    if args.qlora_dir:
        m_q, t_q = load_lora(args.base_for_adapters, args.qlora_dir)
        s, n = 0, 0
        for r in data:
            y = infer(m_q, t_q, r["input"], args.max_new_tokens)
            s += accuracy(y, r["output"])
            n += 1
        print(f"qlora_acc={s/n:.2f}")
