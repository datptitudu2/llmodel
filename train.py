"""
CookBot Training Script
Fine-tune model với LoRA cho hiệu quả và tốc độ
"""

import os
import json
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training

# =============================================================================
# CONFIGURATION
# =============================================================================

# Model
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
OUTPUT_DIR = "models/cookbot-finetuned"

# Dataset
DATASET_PATH = "dataset/train.jsonl"

# Training
EPOCHS = 3
BATCH_SIZE = 2
GRADIENT_ACCUMULATION = 4
LEARNING_RATE = 2e-4
MAX_LENGTH = 2048

# LoRA config
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.1

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_conversation(example):
    """Format conversation từ JSONL sang format model"""
    messages = example["messages"]
    
    # Format theo Phi-3 chat template
    formatted = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "system":
            formatted += f"<|system|>\n{content}<|end|>\n"
        elif role == "user":
            formatted += f"<|user|>\n{content}<|end|>\n"
        elif role == "assistant":
            formatted += f"<|assistant|>\n{content}<|end|>\n"
    
    return {"text": formatted}

def count_samples(filepath):
    """Đếm số samples trong file JSONL"""
    count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for _ in f:
            count += 1
    return count

# =============================================================================
# MAIN TRAINING
# =============================================================================

def main():
    print("=" * 60)
    print("🚀 CookBot Training Script")
    print("=" * 60)
    
    # Check dataset
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Dataset không tồn tại: {DATASET_PATH}")
        print("Chạy: python dataset/generate_dataset.py")
        return
    
    num_samples = count_samples(DATASET_PATH)
    print(f"📊 Dataset: {num_samples} samples")
    
    # Check GPU
    if torch.cuda.is_available():
        print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
        print(f"💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️  Không có GPU, training sẽ chậm!")
    
    # Load tokenizer
    print(f"\n📥 Loading tokenizer: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    # Quantization config (4-bit để tiết kiệm VRAM)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    # Load model
    print(f"📥 Loading model: {MODEL_NAME}")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config if torch.cuda.is_available() else None,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )
    
    # Prepare model for training
    if torch.cuda.is_available():
        model = prepare_model_for_kbit_training(model)
    
    # LoRA config
    print("🔧 Applying LoRA...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load dataset
    print(f"\n📊 Loading dataset: {DATASET_PATH}")
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
    print(f"   Loaded {len(dataset)} samples")
    
    # Format dataset
    print("🔄 Formatting dataset...")
    dataset = dataset.map(format_conversation, remove_columns=["messages"])
    
    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=MAX_LENGTH,
            padding="max_length",
        )
    
    print("🔢 Tokenizing...")
    tokenized_dataset = dataset.map(
        tokenize_function, 
        batched=True,
        remove_columns=["text"]
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION,
        learning_rate=LEARNING_RATE,
        warmup_ratio=0.1,
        logging_steps=10,
        save_steps=100,
        save_total_limit=2,
        fp16=torch.cuda.is_available(),
        optim="adamw_torch",
        report_to="none",
        remove_unused_columns=False,
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )
    
    # Train
    print("\n" + "=" * 60)
    print("🏋️ BẮT ĐẦU TRAINING...")
    print("=" * 60)
    
    trainer.train()
    
    # Save
    print("\n💾 Saving model...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("\n" + "=" * 60)
    print("✅ TRAINING HOÀN THÀNH!")
    print(f"📁 Model saved to: {OUTPUT_DIR}")
    print("=" * 60)
    
    # Instructions
    print("\n📝 Để sử dụng model:")
    print(f"   1. Load model từ: {OUTPUT_DIR}")
    print("   2. Hoặc upload lên Hugging Face Hub")
    print("   3. Cập nhật FINETUNED_MODEL_PATH trong model.py")

if __name__ == "__main__":
    main()

