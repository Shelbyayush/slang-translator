import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer
)
from transformers.utils.quantization_config import BitsAndBytesConfig
from transformers.training_args import (
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from pathlib import Path

def main():
    # --- 1. Configuration ---
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    dataset_path = str(Path("C:\\Users\\Isha\\IdeaProjects\\untitled\\Python\\Projects\\Slang_Translator\\Dataa") / "formatted_dataset.jsonl")
    output_dir = "./models/slang_translator_v1_low_vram"
    
    # --- MODIFIED: Training hyperparameters for lower VRAM usage ---
    num_train_epochs = 1 # Start with 1 epoch for a quick test
    learning_rate = 2e-4
    batch_size = 2 # MODIFIED: Reduced from 4 to 2 to lower memory usage
    gradient_accumulation_steps = 4 # MODIFIED: Increased from 2 to 4 to maintain effective batch size

    # --- 2. Load Data, Model, and Tokenizer ---

    # 4-bit Quantization Configuration (remains the same, already optimized)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=False,
    )

    # --- MODIFIED: LoRA Configuration for lower VRAM ---
    peft_config = LoraConfig(
        lora_alpha=32, # MODIFIED: Adjusted to be 2*r
        lora_dropout=0.1,
        r=16, # MODIFIED: Reduced rank from 64 to 16, this is a major memory saver
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
    )

    print("Loading dataset...")
    dataset = load_dataset("json", data_files=dataset_path, split="train")

    print("Loading model and tokenizer...")
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto" # Automatically maps model to available GPU
    )
    model.config.use_cache = False # Disable caching for training
    model.config.pretraining_tp = 1


    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Prepare model for k-bit training and apply PEFT
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, peft_config)

    # --- 3. Configure Training ---
    print("Configuring training arguments...")
    training_arguments = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        optim="paged_adamw_32bit",
        save_steps=100, # Save a checkpoint every 100 steps
        logging_steps=10, # Log training progress every 10 steps
        learning_rate=learning_rate,
        weight_decay=0.001,
        fp16=False,
        bf16=True, # Use bfloat16 for better performance on modern GPUs
        max_grad_norm=0.3,
        max_steps=-1, # -1 means train for num_train_epochs
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="constant",
        report_to="none" # Can be set to "tensorboard", "wandb", etc.
    )

    # --- 4. Initialize and Start Training ---
    print("Initializing SFTTrainer...")
    trainer = SFTTrainer(
        model = model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="text",
        max_seq_length=256, # MODIFIED: Reduced from 512 to save significant memory
        tokenizer=tokenizer,
        args=training_arguments,
        packing=False, # Packing can be useful for efficiency but set to False for simplicity
    )

    print("Starting training...")
    trainer.train()

    # --- 5. Save the Final Model ---
    final_model_path = Path(output_dir) / "final_checkpoint"
    print(f"Saving the fine-tuned model to {final_model_path}...")
    trainer.save_model(str(final_model_path))

    print("Training complete.")
    print(f"Model saved to {final_model_path}")

if __name__ == "__main__":
    main()
