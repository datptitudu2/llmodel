# Script để merge tất cả file JSONL vào train.jsonl
import os
import glob

def merge_all_jsonl():
    output_file = "train.jsonl"
    all_lines = []
    
    # Tìm tất cả file .jsonl trong các thư mục con
    patterns = [
        "01_core/*.jsonl",
        "02_advanced/*.jsonl", 
        "03_ai_features/*.jsonl"
    ]
    
    for pattern in patterns:
        for filepath in glob.glob(pattern):
            print(f"Reading: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Bỏ qua dòng trống
                        all_lines.append(line)
    
    # Ghi vào file train.jsonl
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    
    print(f"\n=== DONE ===")
    print(f"Total samples: {len(all_lines)}")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    merge_all_jsonl()

