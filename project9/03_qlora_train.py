import argparse
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, DataCollatorForLanguageModeling, Trainer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model

def build_prompt(r):
    return f"Task: Classify the stock headline into Positive, Neutral, or Negative and give a one-line rationale.\nHeadline: {r['input']}\nAnswer format: <Label> | <Rationale>\nAnswer: {r['output']}"

def preprocess(tok, max_len):
    def f(r):
        s = build_prompt(r)
        t = tok(s, truncation=True, padding="max_length", max_length=max_len)
        t["labels"] = t["input_ids"].copy()
        return t
    return f

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--base_model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    p.add_argument("--train_jsonl", default="data/sample_train.jsonl")
    p.add_argument("--output_dir", default="p9_qlora_out")
    p.add_argument("--max_len", type=int, default=512)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--batch", type=int, default=2)
    args = p.parse_args()

    ds = load_dataset("json", data_files=args.train_jsonl)
    tok = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    ds_t = ds["train"].map(preprocess(tok, args.max_len), remove_columns=ds["train"].column_names)

    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="float16", bnb_4bit_quant_type="nf4")
    model = AutoModelForCausalLM.from_pretrained(args.base_model, quantization_config=quant, device_map="auto")
    lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules=["q_proj","k_proj","v_proj","o_proj"])
    model = get_peft_model(model, lora)

    args_tr = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch,
        gradient_accumulation_steps=8,
        learning_rate=args.lr,
        num_train_epochs=args.epochs,
        fp16=True,
        logging_steps=20,
        save_steps=200
    )
    collator = DataCollatorForLanguageModeling(tok, mlm=False)
    trainer = Trainer(model=model, args=args_tr, train_dataset=ds_t, data_collator=collator)
    trainer.train()
    model.save_pretrained(args.output_dir)
