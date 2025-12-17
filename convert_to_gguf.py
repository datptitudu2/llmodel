"""
Convert HuggingFace model sang GGUF
Cách đơn giản: Dùng script Python
"""

import os
import sys
from pathlib import Path

HF_MODEL_PATH = "models/cookbot-merged"
GGUF_OUTPUT = "models/cookshare.gguf"

print("=" * 60)
print("🔄 CONVERT HUGGINGFACE MODEL SANG GGUF")
print("=" * 60)

# Check model path
if not os.path.exists(HF_MODEL_PATH):
    print(f"❌ Không tìm thấy: {HF_MODEL_PATH}")
    print("👉 Giải nén cookbot-merged.zip vào models/cookbot-merged/")
    sys.exit(1)

if not os.path.exists(f"{HF_MODEL_PATH}/model.safetensors"):
    print(f"❌ Không tìm thấy model.safetensors trong {HF_MODEL_PATH}")
    sys.exit(1)

print(f"✅ Tìm thấy model tại: {HF_MODEL_PATH}")

# Check llama.cpp
LLAMA_CPP_PATH = Path("F:/llama.cpp")
if not LLAMA_CPP_PATH.exists():
    print("\n❌ Không tìm thấy llama.cpp tại F:/llama.cpp")
    print("\n📝 Hướng dẫn:")
    print("=" * 60)
    print("""
CÁCH 1: Dùng llama.cpp (Khuyến nghị)

1. Clone llama.cpp (nếu chưa có):
   cd F:\\
   git clone https://github.com/ggerganov/llama.cpp.git

2. Cài transformers:
   pip install transformers

3. Convert:
   cd F:\\llama.cpp
   python convert_hf_to_gguf.py F:\\modelllmchatbot\\models\\cookbot-merged --outfile F:\\modelllmchatbot\\models\\cookshare.gguf --outtype f16

CÁCH 2: Upload lên Hugging Face và dùng convert tool online

1. Tạo repo trên Hugging Face
2. Upload model lên
3. Dùng convert tool online

CÁCH 3: Dùng Colab để convert (Đơn giản nhất!)

1. Upload cookbot-merged lên Google Drive
2. Mở Colab notebook
3. Chạy convert script trên Colab
4. Download GGUF về
    """)
    print("=" * 60)
    sys.exit(1)

# Check transformers
try:
    import transformers
    print(f"✅ transformers version: {transformers.__version__}")
except ImportError:
    print("\n❌ Chưa cài transformers")
    print("👉 Chạy: pip install transformers")
    sys.exit(1)

# Convert
print(f"\n🔄 Converting...")
print(f"   Input: {HF_MODEL_PATH}")
print(f"   Output: {GGUF_OUTPUT}")

convert_script = LLAMA_CPP_PATH / "convert_hf_to_gguf.py"
if not convert_script.exists():
    print(f"❌ Không tìm thấy: {convert_script}")
    sys.exit(1)

# Run convert
import subprocess
cmd = [
    sys.executable,
    str(convert_script),
    os.path.abspath(HF_MODEL_PATH),
    "--outfile",
    os.path.abspath(GGUF_OUTPUT),
    "--outtype",
    "f16"
]

print(f"\n📝 Chạy lệnh:")
print(" ".join(cmd))
print()

try:
    result = subprocess.run(cmd, check=True, cwd=str(LLAMA_CPP_PATH))
    print("\n" + "=" * 60)
    print("✅ CONVERT HOÀN THÀNH!")
    print(f"📁 File: {GGUF_OUTPUT}")
    if os.path.exists(GGUF_OUTPUT):
        size_mb = os.path.getsize(GGUF_OUTPUT) / (1024 * 1024)
        print(f"💾 Size: {size_mb:.1f} MB")
    print("=" * 60)
except subprocess.CalledProcessError as e:
    print(f"\n❌ Lỗi khi convert: {e}")
    print("\n💡 Thử cách khác:")
    print("   1. Cài transformers: pip install transformers")
    print("   2. Chạy lại script này")
    sys.exit(1)

