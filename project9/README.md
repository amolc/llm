# Project 9: Headline Sentiment to Fine‑Tuned LLM (LoRA/QLoRA)

This project walks from a simple prompting baseline to parameter‑efficient fine‑tuning on a small, finance‑oriented dataset. The concrete use‑case is classifying short stock headlines into Positive, Neutral, or Negative with a one‑line rationale.

---

## 1) Setup
- Python 3.10+
- pip install: `transformers datasets peft accelerate bitsandbytes evaluate sentencepiece`
- Optional GPU recommended for training

Project layout:
- data/sample_train.jsonl
- data/sample_eval.jsonl
- 01_baseline_prompt.py
- 02_lora_train.py
- 03_qlora_train.py
- 04_evaluate.py

---

## 2) Baseline (Prompting Only)
Run the baseline classifier with a chat model to establish a reference quality and latency/cost profile.

```bash
python3 01_baseline_prompt.py --text "TCS beats estimates; FY guidance raised"
```

Outputs a label and a short rationale extracted from the model’s text.

---

## 3) Data
The dataset uses instruction style records with fields: instruction, input, output. Labels are Positive, Neutral, Negative followed by a short rationale. Add more rows for better results.

- Edit or extend files under data/.

---

## 4) LoRA Fine‑Tuning
Adapter‑based fine‑tuning on top of a base chat model.

```bash
python3 02_lora_train.py \
  --base_model meta-llama/Llama-2-7b-hf \
  --train_jsonl data/sample_train.jsonl \
  --output_dir p9_lora_out
```

This produces adapter weights in p9_lora_out.

---

## 5) QLoRA Fine‑Tuning
Same task but train LoRA adapters on a 4‑bit quantized base for low VRAM.

```bash
python3 03_qlora_train.py \
  --base_model meta-llama/Llama-2-7b-hf \
  --train_jsonl data/sample_train.jsonl \
  --output_dir p9_qlora_out
```

---

## 6) Evaluation
Evaluate baseline, LoRA, and QLoRA on the same golden set and compare accuracy.

```bash
python3 04_evaluate.py \
  --eval_jsonl data/sample_eval.jsonl \
  --baseline_model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --lora_dir p9_lora_out \
  --qlora_dir p9_qlora_out
```

Reports exact‑label accuracy and prints per‑example predictions.

---

## 7) What To Change
- Replace base_model with a smaller model for CPU or a larger one for quality.
- Grow data/sample_train.jsonl with real headlines from your domain.
- Tighten output format in the prompt if you need JSON outputs.

---

## 8) Learning Goals
- See when prompting is enough.
- Learn how LoRA improves consistency with minimal compute.
- Use QLoRA when VRAM is the bottleneck.

