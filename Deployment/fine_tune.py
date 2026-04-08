import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from pathlib import Path
from huggingface_hub import login
import os

# Authenticate with Hugging Face
hf_token = os.getenv("HUGGINGFACE_HUB_TOKEN")
if hf_token:
    login(token=hf_token)

def main():
    # --- 1. Configuration (Optimized for Llama 3.2 1B) ---
    # Using Llama 3.2 1B for extremely low memory footprint during deployment
    model_id = "meta-llama/Llama-3.2-1B-Instruct" 
    dataset_path = str(Path(__file__).parent.parent / "Dataa" / "formatted_dataset.jsonl")
    output_dir = str(Path(__file__).parent.parent / "models" / "slang_translator_llama_1b")
    
    # Check if GPU is available
    use_gpu = torch.cuda.is_available()
    print(f"GPU available: {use_gpu}")
    device = "cuda" if use_gpu else "cpu"
    
    # Training Hyperparameters
    num_train_epochs = 3 # Increased epochs since 1B model is much faster to train
    learning_rate = 2e-4
    batch_size = 4 if use_gpu else 1  # Reduce batch size for CPU
    gradient_accumulation_steps = 2

    # --- 2. Load Data, Model, and Tokenizer ---

    # 4-bit Quantization (Only if GPU available)
    bnb_config = None
    if use_gpu:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True, # Added double quantization for extra savings
            bnb_4bit_enable_fp32_cpu_offload=True,  # Offload to CPU when GPU memory runs out
        )

    # LoRA Configuration
    peft_config = LoraConfig(
        lora_alpha=32,
        lora_dropout=0.05,
        r=16,
        bias="none",
        task_type="CAUSAL_LM",
        # Expanded target modules for Llama architecture
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )

    print("Loading dataset...")
    dataset = load_dataset("json", data_files=dataset_path, split="train")

    print(f"Loading {model_id}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config if use_gpu else None,
        device_map=device if use_gpu else None,
        token=hf_token,
        trust_remote_code=True,
        max_memory={0: "24GB"} if use_gpu else None,  # Only set max_memory for GPU
        torch_dtype=torch.float32 if not use_gpu else None  # Use float32 for CPU
    )
    if use_gpu:
        model = model.to(device)
    model.config.use_cache = False

    # Load Tokenizer & Fix Padding logic for Llama 3
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Apply PEFT
    if use_gpu:
        model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, peft_config)

    # --- 3. Configure Training ---
    training_arguments = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        optim="paged_adamw_32bit" if use_gpu else "adamw_torch",  # Use standard Adam for CPU
        save_steps=100,
        logging_steps=10,
        learning_rate=learning_rate,
        weight_decay=0.01,
        fp16=False,
        bf16=use_gpu and torch.cuda.is_bf16_supported(),  # Only use bf16 if GPU supports it
        max_grad_norm=0.3,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine", # Cosine scheduler usually works better for Llama
        report_to="none"
    )

    # --- 4. Initialize and Start Training ---
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        args=training_arguments,
        processing_class=tokenizer,
    )

    print("Starting fine-tuning on Llama 3.2 1B...")
    trainer.train()

    # --- 5. Save ---
    trainer.save_model(f"{output_dir}/final_checkpoint")
    print(f"Deployment-ready model saved to {output_dir}")

if __name__ == "__main__":
    main()


''' **Key Differences in this Deployment Version**

1.  **Model Scale:** Switches from a **7-billion** parameter model to a **1-billion** parameter model. This reduces the final model size from ~15GB to ~2.5GB (unquantized) or ~700MB (quantized).
2.  **Target Modules:** Added `gate_proj`, `up_proj`, and `down_proj`. Llama models rely heavily on these MLP layers, so training them ensures the model captures slang nuances better.
3.  **Efficiency:** I enabled `bnb_4bit_use_double_quant`. [cite_start]This quantizes the quantization constants themselves, saving a bit more VRAM during the training and inference phases[cite: 74, 303].
4.  **Learning Schedule:** Changed the `lr_scheduler_type` to `cosine`. Llama 3 models typically show smoother convergence with a cosine decay compared to a constant rate.

---

 **How to Organize Your Repository**

To keep your backup safe, you can structure your local directory like this before pushing to GitHub:

```text
/slang-translator
├── main_branch_files (Mistral)
└── deployment/                <-- New Folder
    └── fine_tune.py           <-- New Llama Script
    └── infer.py               <-- Update this to point to Llama

'''