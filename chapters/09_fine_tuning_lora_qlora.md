# Chapter 9: Fine‑Tuning, LoRA, QLoRA

---

## Overview
- Full fine‑tuning adapts all weights but is compute‑heavy.
- LoRA injects small trainable adapters into attention layers.
- QLoRA performs LoRA on a quantized base model for low VRAM.
- Prefer instruction‑tuning for behavior, domain‑tuning for terminology, and preference‑tuning for style.

---

## When To Fine‑Tune vs. Prompt
- Use prompting/RAG when gaps are knowledge retrieval.
- Fine‑tune when systematic behavior needs changing or domain style must be consistent.
- Use LoRA/QLoRA when GPUs are limited or fast iteration is required.

---

## Data Preparation
- Collect task‑aligned examples (input, expected output).
- Normalize formatting into JSONL with fields like instruction, input, output.
- Deduplicate, filter toxicity/PII, and stratify by intent.

Example row:
```json
{"instruction": "Summarize the earnings call", "input": "Q3 transcript text", "output": "Summary in 5 bullets"}
```

---

## Training Recipes

### Full Fine‑Tuning (baseline)
- Optimizer: AdamW or Adafactor
- LR: 1e‑5 to 3e‑5 for 7B models
- Sequence length set to cover typical inputs

### LoRA
- Target modules: query, key, value, o_proj
- Rank r: 8–32
- Alpha: 16–64
- Dropout: 0–0.1

### QLoRA
- Quantize base to NF4/4‑bit
- Train LoRA on top
- Use paged optimizers to reduce memory

---

## Example: LoRA with PEFT
```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, DataCollatorForLanguageModeling, Trainer
from peft import LoraConfig, get_peft_model

model_name = "meta-llama/Llama-2-7b-hf"
ds = load_dataset("json", data_files="train.jsonl")
tok = AutoTokenizer.from_pretrained(model_name, use_fast=True)
tok.pad_token = tok.eos_token

def format_row(r):
    s = f"Instruction: {r['instruction']}\nInput: {r.get('input','')}\nResponse: {r['output']}"
    t = tok(s, truncation=True, padding="max_length", max_length=1024)
    t["labels"] = t["input_ids"].copy()
    return t

train_ds = ds["train"].map(format_row, remove_columns=ds["train"].column_names)
model = AutoModelForCausalLM.from_pretrained(model_name)
lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules=["q_proj","k_proj","v_proj","o_proj"])
model = get_peft_model(model, lora)

args = TrainingArguments(
    output_dir="out",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=True,
    logging_steps=50,
    save_steps=1000
)

collator = DataCollatorForLanguageModeling(tok, mlm=False)
trainer = Trainer(model=model, args=args, train_dataset=train_ds, data_collator=collator)
trainer.train()
model.save_pretrained("out-adapter")
```

---

## Example: QLoRA (4‑bit)
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="float16", bnb_4bit_quant_type="nf4")
base = "meta-llama/Llama-2-7b-hf"
tok = AutoTokenizer.from_pretrained(base, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(base, quantization_config=quant, device_map="auto")
lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules=["q_proj","k_proj","v_proj","o_proj"])
model = get_peft_model(model, lora)
```

---

## Evaluation
- Exact‑match, BLEU/ROUGE for structured outputs.
- LLM‑as‑a‑judge and rubric scoring for style and safety.
- Check perplexity drift and instruction‑following tests.

---

## Deployment
- Merge adapters for export or keep as delta weights.
- Quantize for serving (int8/int4) when latency sensitive.
- Track lineage: base model, dataset hash, hyperparameters, metrics.

---

## Troubleshooting
- Overfitting: reduce epochs or increase dropout.
- Catastrophic forgetting: mix small percentage of general data.
- Hallucinations: add RAG and groundedness checks.
