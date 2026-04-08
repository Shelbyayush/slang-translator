import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# --- Configuration ---
# Update this to your Hugging Face username/repo once you upload your adapters
ADAPTER_REPO = "Shelbyayush/slang-translator-llama-1b" 
BASE_MODEL = "meta-llama/Llama-3.2-1B-Instruct"

# --- Load Model & Tokenizer ---
print("Loading model... this may take a moment.")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

# We load in 4-bit to fit in the free CPU RAM of HF Spaces
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)

# If you have trained adapters, uncomment the line below:
# model = PeftModel.from_pretrained(model, ADAPTER_REPO)

def translate(formal_text):
    system_msg = "You are a specialized translator. Convert formal English into casual, modern slang."
    prompt = (
        f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        f"{system_msg}<|eot_id|>"
        f"<|start_header_id|>user<|end_header_id|>\n\n"
        f"Translate: {formal_text}<|eot_id|>"
        f"<|start_header_id|>assistant<|end_header_id|>\n\n"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=64,
            temperature=0.7,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )
    
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the assistant's response
    try:
        return decoded.split("assistant")[-1].strip()
    except:
        return decoded

# --- Gradio UI ---
iface = gr.Interface(
    fn=translate,
    inputs=gr.Textbox(lines=2, placeholder="Enter formal sentence here...", label="Formal English"),
    outputs=gr.Textbox(label="Slang Translation"),
    title="Slang-to-Formal AI Translator (Llama 3.2 1B)",
    description="Fine-tuned model for translating professional English into casual slang.",
    examples=["I am currently unavailable to attend the meeting.", "That is an exceptional performance!"]
)

if __name__ == "__main__":
    iface.launch()