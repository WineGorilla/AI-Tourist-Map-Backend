from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

model_id = "openchat/openchat-3.5-0106"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype=torch.float16)
text_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
