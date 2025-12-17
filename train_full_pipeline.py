"""
CookBot Full Training Pipeline
Fine-tune LoRA → Merge → Quantize → GGUF

Quy trình CHUẨN HỌC THUẬT:
1. Fine-tune base model với LoRA adapter
2. Merge LoRA weights vào base model
3. Quantize và convert sang GGUF format
4. Deploy với llama-cpp-python
"""

import os
import json
import torch
import subprocess
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

# Base model - Dùng Qwen2-0.5B vì nhẹ và chất lượng tốt
BASE_MODEL = "Qwen/Qwen2-0.5B-Instruct"

# Paths
DATASET_PATH = "dataset/train.jsonl"
LORA_OUTPUT = "models/cookbot-lora"       # LoRA adapter output
MERGED_OUTPUT = "models/cookbot-merged"    # Merged model output
GGUF_OUTPUT = "models/cookshare.gguf"     # Final GGUF file

# Training hyperparameters
EPOCHS = 3
BATCH_SIZE = 4
GRADIENT_ACCUMULATION = 2
LEARNING_RATE = 2e-4
MAX_LENGTH = 1024

# LoRA config
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05

# Quantization
QUANT_TYPE = "q4_k_m"  # Balance giữa size và quality


# =============================================================================
# STEP 1: FINE-TUNE WITH LoRA
# =============================================================================

def step1_finetune():
    """Fine-tune base model với LoRA"""
    print("\n" + "=" * 60)
    print("📚 STEP 1: FINE-TUNING WITH LoRA")
    print("=" * 60)
    
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
    
    # Check dataset
    if not os.path.exists(DATASET_PATH):
        print(f"❌ Dataset không tồn tại: {DATASET_PATH}")
        print("   Chạy: cd dataset && python merge_all.py")
        return False
    
    # Count samples
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        num_samples = sum(1 for _ in f)
    print(f"📊 Dataset: {num_samples} samples")
    
    # Check GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"💾 VRAM: {vram:.1f} GB")
    else:
        print("⚠️  Không có GPU - Training sẽ chậm!")
    
    # Load tokenizer
    print(f"\n📥 Loading tokenizer: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    
    # Quantization config (4-bit)
    bnb_config = None
    if device == "cuda":
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
    
    # Load model
    print(f"📥 Loading model: {BASE_MODEL}")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto" if device == "cuda" else None,
        trust_remote_code=True,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )
    
    # Prepare for training
    if device == "cuda":
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
    
    # Load and format dataset
    print(f"\n📊 Loading dataset...")
    dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
    
    def format_conversation(example):
        """Format sang ChatML"""
        messages = example["messages"]
        formatted = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            formatted += f"<|im_start|>{role}\n{content}<|im_end|>\n"
        return {"text": formatted}
    
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
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=LORA_OUTPUT,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION,
        learning_rate=LEARNING_RATE,
        warmup_ratio=0.1,
        logging_steps=10,
        save_steps=50,
        save_total_limit=2,
        fp16=device == "cuda",
        optim="adamw_torch",
        report_to="none",
        remove_unused_columns=False,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )
    
    # Train!
    print("\n🏋️ Training...")
    trainer.train()
    
    # Save LoRA adapter
    print(f"\n💾 Saving LoRA adapter to: {LORA_OUTPUT}")
    model.save_pretrained(LORA_OUTPUT)
    tokenizer.save_pretrained(LORA_OUTPUT)
    
    print("✅ Step 1 completed!")
    return True


# =============================================================================
# STEP 2: MERGE LoRA INTO BASE MODEL
# =============================================================================

def step2_merge():
    """Merge LoRA weights vào base model"""
    print("\n" + "=" * 60)
    print("🔀 STEP 2: MERGING LoRA INTO BASE MODEL")
    print("=" * 60)
    
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    
    # Check LoRA output exists
    if not os.path.exists(LORA_OUTPUT):
        print(f"❌ LoRA adapter không tồn tại: {LORA_OUTPUT}")
        return False
    
    # Load tokenizer
    print(f"📥 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(LORA_OUTPUT, trust_remote_code=True)
    
    # Load base model (full precision for merging)
    print(f"📥 Loading base model: {BASE_MODEL}")
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
    )
    
    # Load and merge LoRA
    print(f"🔀 Loading LoRA adapter: {LORA_OUTPUT}")
    model = PeftModel.from_pretrained(base_model, LORA_OUTPUT)
    
    print("🔀 Merging weights...")
    model = model.merge_and_unload()
    
    # Save merged model
    print(f"💾 Saving merged model to: {MERGED_OUTPUT}")
    os.makedirs(MERGED_OUTPUT, exist_ok=True)
    model.save_pretrained(MERGED_OUTPUT, safe_serialization=True)
    tokenizer.save_pretrained(MERGED_OUTPUT)
    
    print("✅ Step 2 completed!")
    return True


# =============================================================================
# STEP 3: QUANTIZE TO GGUF
# =============================================================================

def step3_quantize():
    """Convert và quantize sang GGUF"""
    print("\n" + "=" * 60)
    print("📦 STEP 3: QUANTIZE TO GGUF")
    print("=" * 60)
    
    # Check merged model
    if not os.path.exists(MERGED_OUTPUT):
        print(f"❌ Merged model không tồn tại: {MERGED_OUTPUT}")
        return False
    
    print(f"📦 Converting to GGUF format...")
    print(f"   Input: {MERGED_OUTPUT}")
    print(f"   Output: {GGUF_OUTPUT}")
    print(f"   Quantization: {QUANT_TYPE}")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(GGUF_OUTPUT), exist_ok=True)
    
    # Method 1: Using llama.cpp convert script (recommended)
    print("\n📝 Hướng dẫn convert sang GGUF:")
    print("-" * 50)
    print("""
Bước 1: Clone llama.cpp
    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp

Bước 2: Cài dependencies
    pip install -r requirements.txt

Bước 3: Convert model sang GGUF
    python convert_hf_to_gguf.py ../models/cookbot-merged --outfile ../models/cookshare.gguf --outtype f16

Bước 4: Quantize (giảm size)
    ./llama-quantize ../models/cookshare.gguf ../models/cookshare-q4.gguf q4_k_m

Sau đó rename file cuối cùng thành cookshare.gguf
    """)
    
    # Method 2: Using transformers + llama-cpp-python (alternative)
    print("\n🔄 Hoặc dùng script tự động (cần cài thêm packages):")
    print("-" * 50)
    print("""
pip install transformers torch
pip install llama-cpp-python[server]

# Rồi chạy lại script này với --auto-convert flag
    """)
    
    # Check if llama.cpp exists
    llama_cpp_path = Path("llama.cpp")
    if llama_cpp_path.exists():
        print("\n✅ Tìm thấy llama.cpp, đang convert...")
        try:
            # Convert to GGUF
            convert_script = llama_cpp_path / "convert_hf_to_gguf.py"
            if convert_script.exists():
                subprocess.run([
                    "python", str(convert_script),
                    MERGED_OUTPUT,
                    "--outfile", GGUF_OUTPUT.replace(".gguf", "-f16.gguf"),
                    "--outtype", "f16"
                ], check=True)
                
                # Quantize
                quantize_bin = llama_cpp_path / "llama-quantize"
                if quantize_bin.exists():
                    subprocess.run([
                        str(quantize_bin),
                        GGUF_OUTPUT.replace(".gguf", "-f16.gguf"),
                        GGUF_OUTPUT,
                        QUANT_TYPE
                    ], check=True)
                    
                    print(f"✅ GGUF file created: {GGUF_OUTPUT}")
                    return True
        except Exception as e:
            print(f"⚠️  Lỗi convert: {e}")
    
    print("\n⚠️  Cần convert thủ công theo hướng dẫn trên")
    return True  # Return True to continue


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("🚀 CookBot Full Training Pipeline")
    print("   Fine-tune LoRA → Merge → Quantize → GGUF")
    print("=" * 60)
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", type=int, default=0, help="Run specific step (1, 2, or 3)")
    parser.add_argument("--skip-train", action="store_true", help="Skip training, only merge and quantize")
    args = parser.parse_args()
    
    if args.step == 1 or (args.step == 0 and not args.skip_train):
        if not step1_finetune():
            return
    
    if args.step == 2 or args.step == 0:
        if not step2_merge():
            return
    
    if args.step == 3 or args.step == 0:
        step3_quantize()
    
    print("\n" + "=" * 60)
    print("🎉 PIPELINE HOÀN THÀNH!")
    print("=" * 60)
    print(f"""
📁 Output files:
   - LoRA adapter: {LORA_OUTPUT}/
   - Merged model: {MERGED_OUTPUT}/
   - GGUF file: {GGUF_OUTPUT}

🚀 Để deploy:
   1. Copy {GGUF_OUTPUT} lên Railway
   2. Set environment: GGUF_MODEL_PATH=models/cookshare.gguf
   3. Deploy!

📝 Test local:
   python model.py
    """)


if __name__ == "__main__":
    main()

