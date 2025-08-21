from diffusers import AutoPipelineForText2Image
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

image_pipe = AutoPipelineForText2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    variant="fp16"
).to(device)
