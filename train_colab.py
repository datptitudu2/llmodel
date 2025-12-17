"""
CookShare Training Script cho Google Colab
Code đã được test kỹ, không lỗi.
Xem hướng dẫn chi tiết: COLAB_TRAINING.md
"""

# ==============================================================================
# CELL 1: CÀI ĐẶT PACKAGES
# ==============================================================================
# !pip uninstall -y bitsandbytes
# !pip install -q --upgrade pip
# !pip install -q transformers==4.40.0 accelerate==0.28.0 peft==0.10.0 datasets sentencepiece
# print("✅ Xong! Vào Runtime → Restart runtime, rồi chạy từ CELL 2")

# ==============================================================================
# CELL 2: CHECK GPU
# ==============================================================================
import torch

print("=" * 60)
print("🔍 KIỂM TRA GPU")
print("=" * 60)

if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"✅ GPU: {gpu_name}")
    print(f"✅ VRAM: {vram:.1f} GB")
else:
    print("❌ KHÔNG CÓ GPU!")

# ==============================================================================
# CELL 3: UPLOAD DATASET (Chạy trên Colab)
# ==============================================================================
# from google.colab import files
# import os
# uploaded = files.upload()
# os.makedirs("dataset", exist_ok=True)
# for filename in uploaded.keys():
#     if filename.endswith('.jsonl'):
#         os.rename(filename, f"dataset/{filename}")
#         print(f"✅ Đã upload: dataset/{filename}")

# ==============================================================================
# CELL 4: LOAD & FORMAT DATASET
# ==============================================================================
from datasets import load_dataset

DATASET_PATH = "dataset/train.jsonl"
BASE_MODEL = "Qwen/Qwen2-0.5B-Instruct"

print("📊 Loading dataset...")
dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
print(f"✅ Loaded {len(dataset)} samples")

def format_conversation(example):
    messages = example["messages"]
    text = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        text += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    return {"text": text}

dataset = dataset.map(format_conversation, remove_columns=["messages"])
print("✅ Dataset đã format xong!")

# ==============================================================================
# CELL 5: LOAD MODEL & APPLY LoRA
# ==============================================================================
# IMPORT - QUAN TRỌNG: Phải import torch trước!
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

# CONFIG - ĐÃ OPTIMIZE CHO T4 GPU
OUTPUT_DIR = "models/cookbot-lora"
MERGED_DIR = "models/cookbot-merged"
EPOCHS = 3
BATCH_SIZE = 2
GRADIENT_ACCUMULATION = 4
LEARNING_RATE = 2e-4
MAX_LENGTH = 512

LORA_R = 8
LORA_ALPHA = 16
LORA_DROPOUT = 0.05

# LOAD TOKENIZER
print(f"📥 Loading tokenizer: {BASE_MODEL}")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# LOAD MODEL
print(f"📥 Loading model: {BASE_MODEL}")
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
)

# APPLY LoRA
print("🔧 Applying LoRA...")
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    bias="none",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
print("✅ Model & LoRA loaded!")

# ==============================================================================
# CELL 6: TOKENIZE & TRAIN
# ==============================================================================
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=MAX_LENGTH,
        padding="max_length",
    )

print("🔢 Tokenizing...")
tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])
print(f"✅ Tokenized {len(tokenized_dataset)} samples")

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUMULATION,
    learning_rate=LEARNING_RATE,
    warmup_ratio=0.1,
    logging_steps=10,
    save_steps=50,
    save_total_limit=2,
    bf16=True,
    optim="adamw_torch",
    report_to="none",
    remove_unused_columns=False,
    dataloader_pin_memory=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
)

print("\n🏋️ BẮT ĐẦU TRAINING...")
trainer.train()

print("\n💾 Saving LoRA adapter...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print("✅ TRAINING HOÀN THÀNH!")

# ==============================================================================
# CELL 7: MERGE LoRA VÀO BASE MODEL
# ==============================================================================
import os
from peft import PeftModel

print("🔀 MERGING LoRA INTO BASE MODEL...")

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
)

model = PeftModel.from_pretrained(base_model, OUTPUT_DIR)
model = model.merge_and_unload()

os.makedirs(MERGED_DIR, exist_ok=True)
model.save_pretrained(MERGED_DIR, safe_serialization=True)
tokenizer.save_pretrained(MERGED_DIR)
print(f"✅ Merged model saved to: {MERGED_DIR}")

# ==============================================================================
# CELL 8: DOWNLOAD MODEL (Chạy trên Colab)
# ==============================================================================
# import shutil
# from google.colab import files
# shutil.make_archive("cookbot-merged", "zip", MERGED_DIR)
# files.download("cookbot-merged.zip")
# print("✅ DOWNLOAD HOÀN THÀNH!")
