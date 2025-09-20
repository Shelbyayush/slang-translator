import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from pathlib import Path
import os

def main():
    # Set Hugging Face token for gated model access
    os.environ["HUGGINGFACE_HUB_TOKEN"] = "f_dHMvtQsUlDqCIBaWCSJfpgcsVwnVArbdQw"
    
    # --- 1. Configuration ---
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    dataset_path = str(Path("Dataa/formatted_dataset.jsonl"))
    output_dir = "models/slang_translator_v1"
    
    # Training hyperparameters
    num_train_epochs = 1
    learning_rate = 5e-5
    batch_size = 1
    gradient_accumulation_steps = 4

    print("Loading dataset...")
    dataset = load_dataset("json", data_files=dataset_path, split="train")
    
    # Take a smaller subset for testing
    dataset = dataset.select(range(min(100, len(dataset))))
    print(f"Using {len(dataset)} examples for training")

    print("Loading model and tokenizer...")
    # Load model without quantization for Mac compatibility
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map=None,
        trust_remote_code=True
    )
    
    model = model.to("cpu")
    model.config.use_cache = False

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # LoRA Configuration
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=8,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
    )

    # Apply PEFT
    model = get_peft_model(model, peft_config)

    # Tokenize dataset
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            padding=False,
            max_length=256,
        )
    
    print("Tokenizing dataset...")
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Training arguments
    training_arguments = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        save_steps=25,
        logging_steps=5,
        remove_unused_columns=False,
        dataloader_pin_memory=False,
        dataloader_num_workers=0,
        max_steps=50,
        warmup_steps=5,
        save_total_limit=2,
        report_to=None,
        fp16=False,
        eval_strategy="no",
    )

    # Create trainer
    print("Creating trainer...")
    trainer = Trainer(
        model=model,
        args=training_arguments,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )

    # Train
    print("Starting training...")
    print(f"Model parameters: {model.num_parameters():,}")
    print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    print("Note: Training on Mac will be very slow due to CPU-only processing.")
    
    try:
        trainer.train()
        
        # Save model
        print("Saving model...")
        trainer.model.save_pretrained(f"{output_dir}/final_checkpoint")
        tokenizer.save_pretrained(f"{output_dir}/final_checkpoint")
        
        print(f"Training completed! Model saved to {output_dir}/final_checkpoint")
        
    except Exception as e:
        print(f"Training failed: {e}")
        print("This is expected on Mac due to memory constraints.")
        print("The Mistral 7B model is too large for CPU training.")
        print("Consider using a cloud service with GPU for training.")

if __name__ == "__main__":
    main()
