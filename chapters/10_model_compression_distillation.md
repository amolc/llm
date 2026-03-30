# Chapter 10: Model Compression & Distillation

---

## Goals
- Reduce memory, latency, and cost without sacrificing quality.
- Techniques: quantization, pruning, weight sharing, and knowledge distillation.

---

## Quantization
- Post‑training static quantization: int8 activation and weight scaling.
- 4‑bit quantization (NF4) for large LLMs via bitsandbytes.
- Quantization‑aware training yields better accuracy but requires retraining.

Example (bitsandbytes 4‑bit):
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="float16", bnb_4bit_quant_type="nf4")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", quantization_config=quant, device_map="auto")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", use_fast=True)
```

---

## Pruning
- Magnitude pruning removes lowest‑magnitude weights.
- Structured pruning removes entire heads/neurons for better speedups.
- Fine‑tune after pruning to recover performance.

---

## Weight Sharing & Low‑Rank Factorization
- Decompose weight matrices using low‑rank approximations.
- Ties weights across layers to reduce parameter count at small quality loss.

---

## Knowledge Distillation
- Train a compact student model to mimic a larger teacher.
- Loss combines cross‑entropy on hard labels and KL divergence on teacher logits.

Minimal example:
```python
import torch
from torch.nn import KLDivLoss, CrossEntropyLoss
from transformers import AutoModelForSequenceClassification, AutoTokenizer

teacher = AutoModelForSequenceClassification.from_pretrained("roberta-large", num_labels=3).eval()
student = AutoModelForSequenceClassification.from_pretrained("distilroberta-base", num_labels=3)
tok = AutoTokenizer.from_pretrained("roberta-large")

def distill_step(batch):
    with torch.no_grad():
        t_out = teacher(**batch).logits
    s_out = student(**batch).logits
    kl = KLDivLoss(reduction="batchmean")(torch.log_softmax(s_out/2.0, dim=-1), torch.softmax(t_out/2.0, dim=-1))
    ce = CrossEntropyLoss()(s_out, batch["labels"])
    loss = 0.5*kl + 0.5*ce
    loss.backward()
```

---

## Deployment Formats
- GGUF for llama.cpp CPU/GPU inference.
- TensorRT‑LLM for NVIDIA GPU acceleration.
- ONNX with int8 for edge inference.

---

## Choosing a Strategy
- Memory constrained: 4‑bit quantization or QLoRA adapters.
- Latency constrained: structured pruning and TensorRT‑LLM.
- Tiny devices: distilled students with int8.

---

## Validation Checklist
- Compare perplexity or task metrics before/after compression.
- Evaluate on golden prompts and safety tests.
- Monitor latency (TTFT, tokens/sec) and memory at runtime.
