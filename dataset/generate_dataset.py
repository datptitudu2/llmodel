"""
CookBot Dataset Generator
Tạo dataset training comprehensive với 3 tầng tính năng
"""

import json
import random
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataset.recipes.recipes_database import (
    ALL_RECIPES, MON_BAC, MON_TRUNG, MON_NAM, MON_CHAY, MON_QUOC_TE, MON_NHANH,
    COMMON_ALLERGENS, DIETARY_RESTRICTIONS, COMMON_INGREDIENTS
)

SYSTEM_PROMPT = "Bạn là CookBot - AI tư vấn món ăn của CookShare. Trả lời thân thiện, gợi ý món ăn khi được hỏi."

def save_jsonl(samples, filename):
    """Save samples to JSONL file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        for sample in samples:
            data = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": sample["user"]},
                    {"role": "assistant", "content": sample["assistant"]}
                ]
            }
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    print(f"✅ Saved {len(samples)} samples to {filename}")

# =============================================================================
# TẦNG 1: CORE FEATURES
# =============================================================================

def generate_ingredients_to_recipe():
    """1. Gợi ý công thức từ nguyên liệu"""
    samples = []
    
    # Các tổ hợp nguyên liệu phổ biến
    ingredient_combos = [
        (["trứng", "cà chua", "hành"], ["trung_chien", "mi_xao"]),
        (["thịt bò", "bánh phở", "hành"], ["pho_bo"]),
        (["thịt heo", "bún"], ["bun_cha"]),
        (["tôm", "phở khô", "đậu phộng"], ["pad_thai"]),
        (["gà", "mì quảng", "nghệ"], ["mi_quang"]),
        (["đậu hủ", "nấm", "rau củ"], ["pho_chay", "com_chay"]),
        (["cá", "me", "thơm", "cà chua"], ["canh_chua"]),
        (["thịt ba chỉ", "kim chi"], ["kimchi_jjigae"]),
        (["sườn heo", "gạo tấm"], ["com_tam"]),
        (["bacon", "spaghetti", "trứng"], ["pasta_carbonara"]),
    ]
    
    for ingredients, recipe_ids in ingredient_combos:
        ing_str = ", ".join(ingredients)
        user = f"Mình có {ing_str}, làm món gì được?"
        
        suggestions = []
        for rid in recipe_ids:
            if rid in ALL_RECIPES:
                r = ALL_RECIPES[rid]
                suggestions.append(f"**{r['name']}** ({r['region']}) - {r['time']}, {r['difficulty']}")
        
        assistant = f"Với {ing_str}, mình gợi ý bạn:\n\n"
        for i, s in enumerate(suggestions, 1):
            assistant += f"{i}. {s}\n"
        assistant += "\nBạn muốn mình hướng dẫn chi tiết món nào không? 😊"
        
        samples.append({"user": user, "assistant": assistant})
    
    # Thêm các variations
    more_samples = [
        {
            "user": "Trong tủ lạnh còn mỗi trứng và cà chua thôi",
            "assistant": "Đơn giản mà ngon! 🍳 Mình gợi ý:\n\n1. **Trứng chiên cà chua** - 10 phút, Dễ\n   - Xào cà chua với trứng, nêm nước mắm\n   - Ăn với cơm nóng là tuyệt vời!\n\n2. **Canh cà chua trứng** - 15 phút, Dễ\n   - Đun nước sôi, cho cà chua\n   - Đập trứng vào, nêm gia vị\n\nBạn thích món nào? Mình hướng dẫn chi tiết ngay! 😊"
        },
        {
            "user": "Có gạo, thịt heo, trứng làm gì ngon?",
            "assistant": "Nguyên liệu cơ bản nhưng làm được nhiều món ngon lắm! 🍚\n\n1. **Cơm chiên** - 15 phút, Dễ\n   - Chiên cơm với thịt băm, trứng\n   - Nêm nước tương, tiêu\n\n2. **Cơm tấm sườn** - 1 giờ, Trung bình\n   - Ướp thịt nướng, chiên trứng ốp la\n   - Ăn với cơm tấm, đồ chua\n\n3. **Cháo thịt bằm trứng** - 30 phút, Dễ\n   - Nấu cháo với thịt băm\n   - Thêm trứng khuấy\n\nBạn chọn món nào? 😊"
        },
        {
            "user": "Tối nay có mỗi đậu hủ với nấm, nấu gì cho ngon?",
            "assistant": "Đậu hủ với nấm là combo tuyệt vời cho món chay! 🥗\n\n1. **Đậu hủ xào nấm** - 20 phút, Dễ\n   - Chiên đậu hủ vàng, xào với nấm\n   - Nêm nước tương, tiêu\n   - Rắc hành lá\n\n2. **Canh đậu hủ nấm** - 25 phút, Dễ\n   - Nấu nước dùng từ nấm\n   - Cho đậu hủ non vào\n   - Thêm rau cải\n\n3. **Phở chay đậu hủ nấm** - 1 giờ, Dễ\n   - Nước dùng từ rau củ, nấm\n   - Topping đậu hủ chiên, nấm xào\n\nMón nào hấp dẫn bạn? 😊"
        },
    ]
    samples.extend(more_samples)
    
    return samples

def generate_step_by_step():
    """2. Hướng dẫn nấu từng bước"""
    samples = []
    
    for recipe_id, recipe in ALL_RECIPES.items():
        # Câu hỏi về cách nấu
        questions = [
            f"Cách nấu {recipe['name']}?",
            f"Hướng dẫn làm {recipe['name']} đi",
            f"Làm {recipe['name']} như thế nào?",
        ]
        
        for q in questions[:1]:  # Chỉ lấy 1 variation để tránh quá nhiều
            # Format ingredients
            ing_list = []
            for ing_name, ing_info in recipe["ingredients"].items():
                ing_list.append(f"- {ing_name.replace('_', ' ')}: {ing_info['amount']} {ing_info['unit']}")
            
            # Format steps
            steps_list = []
            for i, step in enumerate(recipe["steps"], 1):
                steps_list.append(f"**Bước {i}:** {step}")
            
            # Format tips
            tips_str = ""
            if "tips" in recipe:
                tips_str = "\n\n**💡 Mẹo:**\n"
                for tip in recipe["tips"]:
                    tips_str += f"- {tip}\n"
            
            assistant = f"Mình hướng dẫn bạn làm **{recipe['name']}** nhé! 🍳\n\n"
            assistant += f"⏱ Thời gian: {recipe['time']} | 📊 Độ khó: {recipe['difficulty']} | 👥 Khẩu phần: {recipe['servings']} người\n\n"
            assistant += "**📝 Nguyên liệu:**\n"
            assistant += "\n".join(ing_list[:8])  # Giới hạn 8 nguyên liệu
            assistant += "\n\n**👨‍🍳 Cách làm:**\n"
            assistant += "\n".join(steps_list)
            assistant += tips_str
            assistant += "\n\nBạn có câu hỏi gì về món này không? 😊"
            
            samples.append({"user": q, "assistant": assistant})
    
    return samples

def generate_substitutions():
    """3. Thay thế nguyên liệu"""
    samples = []
    
    # Các câu hỏi thay thế phổ biến
    substitution_qa = [
        {
            "user": "Không có bơ thì thay bằng gì?",
            "assistant": "Không có bơ? Không sao! 🧈 Mình gợi ý:\n\n**Thay thế bơ:**\n1. **Dầu ô liu** - Tỷ lệ 3/4 (0.75 phần dầu = 1 phần bơ)\n2. **Dầu dừa** - Tỷ lệ 1:1, cho vị béo ngậy\n3. **Bơ thực vật** - Tỷ lệ 1:1, rẻ hơn\n4. **Kem phô mai** - Cho bánh mềm hơn\n\n**Lưu ý:** Nếu làm bánh, dầu sẽ cho kết quả khác một chút. Bơ cho bánh giòn, dầu cho bánh mềm.\n\nBạn đang làm món gì? Mình tư vấn cụ thể hơn! 😊"
        },
        {
            "user": "Ăn chay thì thay thịt bằng gì?",
            "assistant": "Ăn chay vẫn đủ chất nhé! 🥗 Mình gợi ý:\n\n**Thay thế thịt:**\n1. **Đậu hủ** - Protein cao, dễ chế biến\n2. **Nấm đông cô** - Dai, thơm như thịt\n3. **Đậu hủ ki (da đậu)** - Kết cấu như thịt\n4. **Seitan (mì căn)** - Protein rất cao\n5. **Tempeh** - Đậu nành lên men, bổ dưỡng\n\n**Mẹo:**\n- Ướp đậu hủ với nước tương để có vị\n- Nấm xào cháy cạnh sẽ giống thịt hơn\n\nBạn muốn làm món chay nào? 😊"
        },
        {
            "user": "Không có nước mắm thay bằng gì?",
            "assistant": "Không có nước mắm? Thay thế được! 🐟\n\n**Thay thế nước mắm:**\n1. **Nước tương + muối** - Tỷ lệ 1:1, thêm chút muối\n2. **Mắm tôm pha loãng** - Cho món Huế\n3. **Muối + đường** - Cơ bản nhất\n4. **Nước tương Nhật** - Cho món Á\n5. **Dashi + muối** - Cho vị umami\n\n**Lưu ý:**\n- Nước mắm có vị umami đặc trưng\n- Thay thế sẽ hơi khác vị gốc\n- Nếu làm món Việt, nên mua nước mắm nhé!\n\nBạn đang làm món gì? 😊"
        },
        {
            "user": "Dị ứng hải sản, nấu phở thay nước mắm bằng gì?",
            "assistant": "Dị ứng hải sản mà muốn ăn phở? Được luôn! 🍜\n\n**Thay nước mắm trong phở:**\n1. **Muối + đường** - Tỷ lệ 1 muỗng muối + 1/2 muỗng đường\n2. **Nước tương loãng** - 2 muỗng nước tương + 1 muỗng nước\n3. **Muối hầm xương** - Dùng muối hồng/muối biển\n\n**Mẹo cho phở không nước mắm:**\n- Tăng thời gian ninh xương để ngọt tự nhiên\n- Thêm củ cải, cà rốt vào nước dùng\n- Nướng hành gừng kỹ hơn để thơm\n\n⚠️ **Lưu ý an toàn:** Kiểm tra thành phần các gia vị, nhiều loại có chứa hải sản.\n\nBạn cần mình hướng dẫn công thức phở không nước mắm không? 😊"
        },
        {
            "user": "Thay trứng bằng gì khi làm bánh?",
            "assistant": "Làm bánh không trứng vẫn ngon! 🥚➡️\n\n**Thay 1 quả trứng:**\n1. **Chuối chín nghiền** - 1/2 quả (cho bánh mềm)\n2. **Táo nghiền** - 1/4 cup (cho bánh muffin)\n3. **Sữa chua** - 1/4 cup (cho bánh xốp)\n4. **Bột lanh + nước** - 1 muỗng bột + 3 muỗng nước\n5. **Aquafaba** - 3 muỗng nước đậu gà (thay lòng trắng)\n\n**Tùy loại bánh:**\n- Bánh mì: Dùng bột lanh\n- Bánh ngọt: Dùng chuối hoặc táo\n- Bánh bông lan: Dùng aquafaba\n\nBạn đang làm bánh gì? Mình tư vấn cụ thể! 🎂"
        },
    ]
    samples.extend(substitution_qa)
    
    # Generate từ database
    for recipe_id, recipe in ALL_RECIPES.items():
        if "substitutions" in recipe:
            for orig, subs in recipe["substitutions"].items():
                user = f"Làm {recipe['name']} mà không có {orig.replace('_', ' ')} thì sao?"
                subs_str = ", ".join(subs[:3])
                assistant = f"Không có {orig.replace('_', ' ')} để làm {recipe['name']}? Không sao! 😊\n\n**Thay thế:**\n"
                for i, s in enumerate(subs[:3], 1):
                    assistant += f"{i}. **{s}**\n"
                assistant += f"\n**Mẹo:** Tùy nguyên liệu thay thế, vị sẽ hơi khác gốc. Nhưng vẫn ngon!\n\nBạn muốn mình hướng dẫn cách làm với nguyên liệu thay thế không? 😊"
                samples.append({"user": user, "assistant": assistant})
    
    return samples[:30]  # Giới hạn số lượng

def generate_portion_scaling():
    """4. Điều chỉnh khẩu phần"""
    samples = []
    
    scaling_qa = [
        {
            "user": "Công thức phở bò cho 4 người, mình nấu cho 1 người thôi",
            "assistant": "Mình tính lại khẩu phần cho 1 người nhé! 🍜\n\n**Phở Bò - 1 người (chia 4):**\n\n📝 **Nguyên liệu:**\n- Xương bò: 250g (hoặc dùng nước dùng có sẵn)\n- Thịt bò tái: 75g\n- Bánh phở: 125g\n- Hành tây: 1/2 củ\n- Gừng: 1/4 củ\n- Gia vị: giảm 1/4\n\n💡 **Mẹo nấu 1 người:**\n- Nên mua nước dùng có sẵn (tiết kiệm)\n- Hoặc ninh xương 1 lần, chia ra đông đá\n- Thịt bò mua vừa đủ, thái mỏng\n\nBạn cần mình hướng dẫn chi tiết không? 😊"
        },
        {
            "user": "Nấu cơm tấm cho 10 người được không?",
            "assistant": "Nấu tiệc đông vui ha! 🍚 Mình scale lên 10 người nhé!\n\n**Cơm Tấm - 10 người (x2.5 từ 4 người):**\n\n📝 **Nguyên liệu:**\n- Gạo tấm: 1kg\n- Sườn heo: 10 miếng\n- Bì heo: 500g\n- Trứng: 10 quả\n- Đồ chua: 500g\n- Nước mắm pha: 250ml\n\n💡 **Mẹo nấu đông người:**\n- Ướp sườn từ tối hôm trước\n- Nấu cơm bằng nồi cơm điện lớn\n- Chiên trứng theo batch\n- Pha nước mắm sẵn 1 tô lớn\n\n⏱ **Thời gian:** Chuẩn bị 1.5 giờ, nấu 1 giờ\n\nBạn cần mình tính chi phí ước tính không? 😊"
        },
        {
            "user": "Làm bún chả cho 2 người",
            "assistant": "Bún chả cho 2 người, vừa đủ ăn! 🍖\n\n**Bún Chả - 2 người (chia 2 từ 4 người):**\n\n📝 **Nguyên liệu:**\n- Thịt ba chỉ: 150g\n- Thịt nạc vai: 150g\n- Bún tươi: 250g\n- Nước mắm: 50ml\n- Đường: 40g\n- Tỏi: 2-3 tép\n- Rau sống: 100g\n\n👨‍🍳 **Mẹo:**\n- Ướp thịt 30 phút là đủ\n- Nướng bếp gas nếu không có than\n- Làm nước chấm vừa đủ dùng\n\n💰 **Chi phí ước tính:** ~60,000đ cho 2 người\n\nCần mình hướng dẫn chi tiết cách làm không? 😊"
        },
    ]
    samples.extend(scaling_qa)
    
    return samples

def generate_allergy_warnings():
    """5. Cảnh báo dị ứng / kiêng kỵ"""
    samples = []
    
    allergy_qa = [
        {
            "user": "Mình dị ứng hải sản, có ăn được bún bò Huế không?",
            "assistant": "⚠️ **CẢNH BÁO DỊ ỨNG!**\n\nBún bò Huế truyền thống có **mắm ruốc** (làm từ tôm/tép), nên **KHÔNG PHÙ HỢP** với người dị ứng hải sản!\n\n**Chi tiết thành phần có hải sản:**\n- Mắm ruốc (tôm tép)\n- Chả cua (nếu có)\n\n**Giải pháp:**\n1. Làm bún bò Huế KHÔNG mắm ruốc\n   - Thay bằng mắm + muối + ớt\n   - Vẫn có vị cay đậm đà\n2. Bỏ chả cua, thay bằng chả lụa\n3. Hỏi kỹ nhà hàng trước khi ăn\n\nBạn muốn mình hướng dẫn công thức bún bò Huế an toàn cho người dị ứng hải sản không? 😊"
        },
        {
            "user": "Món nào phù hợp cho người tiểu đường?",
            "assistant": "Người tiểu đường cần chú ý chỉ số đường huyết! 🩺\n\n**MÓN NÊN ĂN:**\n1. **Phở/Bún với ít bánh** - Tăng rau, giảm carb\n2. **Cá nướng/hấp** - Protein tốt, ít calo\n3. **Rau xào** - Nhiều chất xơ\n4. **Canh chua** - Ít đường tự nhiên\n5. **Gà luộc** - Protein nạc\n\n**MÓN NÊN TRÁNH:**\n❌ Cơm trắng nhiều\n❌ Bánh mì, bánh ngọt\n❌ Nước ngọt, trà sữa\n❌ Trái cây ngọt (xoài, sầu riêng)\n\n**MẸO:**\n- Thay cơm trắng bằng cơm gạo lứt\n- Ăn nhiều rau trước, rồi mới ăn cơm\n- Chia nhỏ bữa ăn\n\nBạn muốn mình gợi ý thực đơn tuần cho người tiểu đường không? 😊"
        },
        {
            "user": "Con mình 3 tuổi, có món nào không nên cho bé ăn?",
            "assistant": "Trẻ nhỏ cần được bảo vệ! 👶 Mình liệt kê:\n\n**❌ MÓN KHÔNG NÊN CHO TRẺ 3 TUỔI:**\n\n1. **Món cay** (bún bò Huế, kim chi...)\n   - Gây kích ứng dạ dày\n   - Có thể gây dị ứng\n\n2. **Hải sản sống** (sushi, gỏi cá...)\n   - Nguy cơ nhiễm khuẩn\n   - Dị ứng cao\n\n3. **Đồ ăn có rượu** (rượu nấu, bò sốt vang...)\n   - Dù nấu chín vẫn còn cồn\n\n4. **Hạt nhỏ tròn** (đậu phộng nguyên hạt, nho...)\n   - Nguy cơ hóc\n\n5. **Mật ong** (nếu dưới 1 tuổi)\n\n**✅ MÓN AN TOÀN:**\n- Cháo, súp mềm\n- Cơm nát với thịt băm\n- Rau củ nấu mềm\n- Trái cây nghiền\n\nBạn muốn mình gợi ý thực đơn cho bé không? 😊"
        },
        {
            "user": "Mình ăn chay trường, gợi ý món đi",
            "assistant": "Ăn chay trường vẫn đầy đủ dinh dưỡng! 🥗\n\n**GỢI Ý MÓN CHAY:**\n\n🍜 **Món nước:**\n- Phở chay (đậu hủ, nấm)\n- Bún riêu chay\n- Hủ tiếu chay\n\n🍚 **Món cơm:**\n- Cơm chiên chay\n- Cơm thập cẩm chay\n- Cơm cuộn rong biển\n\n🥘 **Món xào:**\n- Đậu hủ sốt cà chua\n- Nấm xào thập cẩm\n- Rau củ xào\n\n⚠️ **LƯU Ý:**\n- Kiểm tra nước mắm (có cá) → dùng nước tương\n- Kiểm tra dầu hào (có hàu) → bỏ qua\n- Mắm tôm, mắm ruốc → không dùng\n\n**BỔ SUNG PROTEIN:**\n- Đậu hủ, tempeh, đậu lăng\n- Nấm, rau cải, đậu các loại\n\nBạn muốn mình hướng dẫn công thức món chay nào? 😊"
        },
        {
            "user": "Dị ứng đậu phộng có ăn được Pad Thai không?",
            "assistant": "⚠️ **CẢNH BÁO DỊ ỨNG ĐẬU PHỘNG!**\n\nPad Thai truyền thống **CÓ ĐẬU PHỘNG** rang rắc lên trên!\n\n**KHÔNG AN TOÀN** nếu bạn dị ứng đậu phộng.\n\n**Giải pháp:**\n1. **Tự nấu tại nhà:**\n   - Bỏ đậu phộng\n   - Thay bằng hạt điều (nếu không dị ứng)\n   - Hoặc bỏ hẳn\n\n2. **Ăn ngoài:**\n   - Thông báo nhà hàng về dị ứng\n   - Yêu cầu không cho đậu phộng\n   - Hỏi về cross-contamination\n\n**⚠️ Cẩn thận:**\n- Sauce Pad Thai có thể có đậu phộng xay\n- Dầu chiên có thể dùng chung\n\nBạn muốn mình hướng dẫn Pad Thai không đậu phộng không? 😊"
        },
    ]
    samples.extend(allergy_qa)
    
    return samples

# =============================================================================
# TẦNG 2: NÂNG CAO
# =============================================================================

def generate_meal_planning():
    """6. Lên lịch ăn (meal plan)"""
    samples = []
    
    meal_plan_qa = [
        {
            "user": "Lên thực đơn tuần cho mình đi",
            "assistant": "Mình lên thực đơn tuần đầy đủ dinh dưỡng nhé! 📅\n\n**THỨ 2:**\n🌅 Sáng: Phở bò\n🌞 Trưa: Cơm + Cá kho + Canh rau\n🌙 Tối: Bún chả\n\n**THỨ 3:**\n🌅 Sáng: Bánh mì ốp la\n🌞 Trưa: Cơm tấm sườn bì chả\n🌙 Tối: Canh chua cá + Cơm\n\n**THỨ 4:**\n🌅 Sáng: Bún bò Huế\n🌞 Trưa: Cơm + Thịt kho tàu + Rau luộc\n🌙 Tối: Mì xào hải sản\n\n**THỨ 5:**\n🌅 Sáng: Cháo gà\n🌞 Trưa: Hủ tiếu\n🌙 Tối: Lẩu (cuối tuần sớm!)\n\n**THỨ 6:**\n🌅 Sáng: Bánh cuốn\n🌞 Trưa: Cơm + Gà kho gừng\n🌙 Tối: Bánh xèo\n\n**THỨ 7:**\n🌅 Sáng: Xôi\n🌞 Trưa: Bún riêu\n🌙 Tối: BBQ tại nhà\n\n**CHỦ NHẬT:**\n🌅 Sáng: Phở gà\n🌞 Trưa: Cơm gia đình\n🌙 Tối: Ăn nhẹ (cháo, súp)\n\nBạn muốn mình điều chỉnh theo sở thích không? 😊"
        },
        {
            "user": "Thực đơn cho người ăn kiêng giảm cân",
            "assistant": "Thực đơn giảm cân healthy nhưng vẫn ngon! 💪\n\n**NGUYÊN TẮC:**\n- Giảm tinh bột, tăng protein\n- Nhiều rau xanh\n- Ít dầu mỡ\n- ~1500 calo/ngày\n\n**THỰC ĐƠN MẪU:**\n\n🌅 **Sáng (400 calo):**\n- Trứng luộc + rau xà lách\n- Hoặc: Cháo yến mạch + trái cây\n\n🌞 **Trưa (500 calo):**\n- Ức gà nướng + salad\n- Hoặc: Cá hấp + rau luộc + 1/2 chén cơm gạo lứt\n\n🍎 **Xế (100 calo):**\n- Trái cây ít đường (táo, cam)\n- Hoặc: Sữa chua không đường\n\n🌙 **Tối (400 calo):**\n- Súp rau củ + thịt nạc\n- Hoặc: Salad + cá hồi\n\n**MẸO:**\n- Uống nước trước bữa ăn\n- Ăn chậm, nhai kỹ\n- Không ăn sau 7 giờ tối\n\nBạn cần mình chi tiết món nào không? 😊"
        },
        {
            "user": "Gợi ý bữa sáng healthy cho cả tuần",
            "assistant": "Bữa sáng healthy, nhanh gọn cho cả tuần! 🌅\n\n**THỨ 2:** Smoothie chuối + yến mạch + sữa\n⏱ 5 phút | 350 calo\n\n**THỨ 3:** Trứng ốp la + bánh mì nguyên cám + bơ\n⏱ 10 phút | 400 calo\n\n**THỨ 4:** Cháo yến mạch + hạt chia + trái cây\n⏱ 10 phút | 320 calo\n\n**THỨ 5:** Sandwich trứng + rau + phô mai\n⏱ 10 phút | 380 calo\n\n**THỨ 6:** Sữa chua Hy Lạp + granola + mật ong\n⏱ 3 phút | 350 calo\n\n**THỨ 7:** Pancake chuối + mật ong\n⏱ 15 phút | 420 calo\n\n**CHỦ NHẬT:** Phở/Bún (reward day!)\n⏱ 30 phút | 450 calo\n\n**MẸO MEAL PREP:**\n- Cắt trái cây sẵn từ tối\n- Luộc trứng sẵn 3-4 quả\n- Chuẩn bị granola cho cả tuần\n\nBạn thích món sáng nào nhất? 😊"
        },
    ]
    samples.extend(meal_plan_qa)
    
    return samples

def generate_weather_suggestions():
    """7. Gợi ý theo thời tiết"""
    samples = []
    
    weather_qa = [
        {
            "user": "Trời lạnh quá, ăn gì cho ấm?",
            "assistant": "Trời lạnh thì phải ăn món nóng hổi! ❄️🔥\n\n**MÓN ẤM NGƯỜI:**\n\n1. **Phở bò** 🍜\n   - Nước dùng nóng, thịt bò tái\n   - Thêm gừng, hành cho ấm\n\n2. **Lẩu** 🍲\n   - Lẩu thái cay, lẩu gà lá é\n   - Ăn cùng gia đình ấm cúng\n\n3. **Bún bò Huế** 🌶️\n   - Cay nồng, đậm đà\n   - Nước dùng xương hầm\n\n4. **Cháo nóng** 🥣\n   - Cháo gà, cháo lươn\n   - Thêm gừng, tiêu\n\n5. **Canh xương hầm** 🥘\n   - Xương heo hầm rau củ\n   - Ngọt tự nhiên, ấm bụng\n\n**ĐỒ UỐNG ẤM:**\n- Trà gừng + mật ong\n- Nước chanh nóng\n- Sữa nóng\n\nBạn muốn mình hướng dẫn món nào? 😊"
        },
        {
            "user": "Hôm nay nóng 38 độ, ăn gì cho mát?",
            "assistant": "38 độ nóng kinh! ☀️ Ăn món mát giải nhiệt nhé!\n\n**MÓN MÁT:**\n\n1. **Gỏi cuốn** 🥗\n   - Tươi mát, nhiều rau\n   - Chấm mắm me chua ngọt\n\n2. **Bún thịt nướng** 🍜\n   - Ăn nguội với rau sống\n   - Nước mắm chua ngọt\n\n3. **Canh chua** 🍲\n   - Chua mát, giải nhiệt\n   - Nhiều rau, cà chua\n\n4. **Salad trái cây** 🍉\n   - Dưa hấu, xoài, thanh long\n   - Thêm chút muối ớt\n\n5. **Chè đậu xanh** 🍨\n   - Ướp lạnh, giải khát\n   - Bổ sung năng lượng\n\n**ĐỒ UỐNG:**\n- Nước chanh đá\n- Trà đá\n- Sinh tố (bơ, xoài, dừa)\n\n**LƯU Ý:** Tránh đồ cay nóng, nhiều dầu mỡ!\n\nBạn thích món nào? 😊"
        },
        {
            "user": "Trời mưa, gợi ý món ngon",
            "assistant": "Trời mưa lành lạnh, ăn gì cho ấm cúng! 🌧️\n\n**MÓN HAY ĂN NGÀY MƯA:**\n\n1. **Bánh xèo** 🥞\n   - Giòn tan, nhân đầy đặn\n   - Ăn kèm rau sống\n   - \"Mưa rơi nhớ bánh xèo!\"\n\n2. **Cháo nóng** 🥣\n   - Cháo lòng, cháo gà\n   - Ấm bụng, dễ ăn\n\n3. **Mì tôm trứng** 🍜\n   - Đơn giản mà ngon\n   - Thêm rau, thịt\n\n4. **Súp nóng** 🍵\n   - Súp cua, súp gà\n   - Ấm áp, bổ dưỡng\n\n5. **Lẩu** 🍲\n   - Sum họp gia đình\n   - Nhiều loại: thái, Hàn, Việt\n\n**COMBO HOÀN HẢO:**\n☔ Trời mưa + Bánh xèo + Trà nóng = Perfect!\n\nBạn muốn mình hướng dẫn làm bánh xèo không? 😊"
        },
    ]
    samples.extend(weather_qa)
    
    return samples

def generate_shopping_list():
    """8. Tạo danh sách đi chợ"""
    samples = []
    
    shopping_qa = [
        {
            "user": "Mình muốn nấu phở bò, liệt kê đi chợ giúp",
            "assistant": "Đây là danh sách đi chợ cho Phở Bò (4 người)! 🛒\n\n**🥩 THỊT/XƯƠNG:**\n- [ ] Xương bò: 1kg\n- [ ] Thịt bò tái: 300g\n\n**🍜 BÚN/PHỞ:**\n- [ ] Bánh phở tươi: 500g\n\n**🧅 RAU CỦ:**\n- [ ] Hành tây: 2 củ\n- [ ] Gừng: 1 củ\n- [ ] Hành lá: 1 bó\n- [ ] Ngò gai: 1 bó\n- [ ] Giá đỗ: 200g\n- [ ] Chanh: 2 quả\n- [ ] Ớt: vài quả\n\n**🧂 GIA VỊ:**\n- [ ] Quế: 2 thanh\n- [ ] Hồi: 3-4 cánh\n- [ ] Nước mắm\n- [ ] Muối\n\n**💰 CHI PHÍ ƯỚC TÍNH:** ~270,000đ\n\n**💡 MẸO:**\n- Mua xương bò ở chợ rẻ hơn siêu thị\n- Thịt bò nên mua tươi, không đông đá\n\nBạn cần thêm gì nữa không? 😊"
        },
        {
            "user": "Lên danh sách đi chợ cho thực đơn cả tuần",
            "assistant": "Danh sách đi chợ cho 1 tuần (2 người)! 🛒📝\n\n**🥩 THỊT/CÁ (mua 1-2 lần/tuần):**\n- [ ] Thịt heo (ba chỉ + nạc): 1kg\n- [ ] Thịt gà: 1 con hoặc 500g ức\n- [ ] Cá: 500g (tùy loại)\n- [ ] Tôm: 300g\n- [ ] Trứng: 1 vỉ (10 quả)\n\n**🍚 TINH BỘT:**\n- [ ] Gạo: 2kg\n- [ ] Bún/Phở: 500g\n- [ ] Mì: 5 gói\n\n**🥬 RAU CỦ (mua 2-3 lần/tuần):**\n- [ ] Rau cải: 2-3 bó\n- [ ] Cà chua: 500g\n- [ ] Hành tây: 5-6 củ\n- [ ] Cà rốt: 3-4 củ\n- [ ] Khoai tây: 500g\n- [ ] Giá đỗ: 300g\n- [ ] Rau thơm: 2-3 bó\n\n**🍎 TRÁI CÂY:**\n- [ ] Chuối, cam, táo\n\n**🧂 GIA VỊ (kiểm tra còn không):**\n- [ ] Nước mắm, nước tương\n- [ ] Dầu ăn\n- [ ] Muối, đường, tiêu\n- [ ] Tỏi, ớt, gừng\n\n**💰 TỔNG ƯỚC TÍNH:** ~600,000 - 800,000đ\n\nBạn cần điều chỉnh gì không? 😊"
        },
    ]
    samples.extend(shopping_qa)
    
    return samples

def generate_cost_estimation():
    """9. Ước tính chi phí"""
    samples = []
    
    cost_qa = [
        {
            "user": "Nấu phở bò tốn bao nhiêu tiền?",
            "assistant": "Mình tính chi phí Phở Bò (4 người) nhé! 💰\n\n**CHI TIẾT CHI PHÍ:**\n\n🥩 **Thịt/Xương:**\n- Xương bò 1kg: 80,000đ\n- Thịt bò tái 300g: 120,000đ\n\n🍜 **Bánh phở:**\n- Bánh phở 500g: 25,000đ\n\n🧅 **Rau củ:**\n- Hành tây, gừng: 15,000đ\n- Rau thơm, giá: 20,000đ\n- Chanh, ớt: 8,000đ\n\n🧂 **Gia vị:**\n- Quế, hồi, nước mắm: 15,000đ\n\n**💵 TỔNG: ~283,000đ (4 người)**\n**👤 TRUNG BÌNH: ~71,000đ/người**\n\n📊 **SO SÁNH:**\n- Ăn quán: 50-80k/tô\n- Tự nấu: ~71k/người + dư nước dùng!\n\n**💡 MẸO TIẾT KIỆM:**\n- Mua xương bò ở chợ: rẻ hơn 20%\n- Ninh nhiều nước dùng, đông đá dùng dần\n\nBạn muốn biết chi phí món nào khác không? 😊"
        },
        {
            "user": "Chi phí ăn uống 1 tuần khoảng bao nhiêu?",
            "assistant": "Mình tính chi phí ăn uống 1 tuần (2 người) nhé! 💰📊\n\n**CHI PHÍ THEO MỨC:**\n\n💚 **TIẾT KIỆM (~500k-700k/tuần/2 người):**\n- Nấu ăn nhà 100%\n- Ưu tiên món đơn giản\n- Mua chợ, không siêu thị\n\n💛 **VỪA PHẢI (~800k-1.2tr/tuần/2 người):**\n- Nấu nhà 70%, ăn ngoài 30%\n- Đa dạng món\n- Có hải sản 1-2 lần\n\n🧡 **THOẢI MÁI (~1.5tr-2tr/tuần/2 người):**\n- Nấu nhà 50%, ăn ngoài 50%\n- Món ngon, chất lượng\n- Hải sản, thịt bò thường xuyên\n\n**CHI TIẾT (mức vừa phải):**\n- Thịt/cá: 300,000đ\n- Rau củ: 150,000đ\n- Gạo, bún, mì: 50,000đ\n- Gia vị: 50,000đ\n- Ăn ngoài 2-3 bữa: 300,000đ\n- **TỔNG: ~850,000đ**\n\nBạn muốn mình lên thực đơn theo budget cụ thể không? 😊"
        },
    ]
    samples.extend(cost_qa)
    
    return samples

# =============================================================================
# TẦNG 3: AI THẬT
# =============================================================================

def generate_user_preferences():
    """10. Nhớ sở thích người dùng"""
    samples = []
    
    pref_qa = [
        {
            "user": "Mình không ăn được cay, nhớ giúp nhé",
            "assistant": "Đã ghi nhớ rồi nhé! ✅\n\n**Sở thích của bạn:**\n❌ Không ăn cay\n\nTừ giờ mình sẽ:\n- Gợi ý món không cay\n- Nhắc bạn điều chỉnh gia vị\n- Đề xuất thay thế nếu món gốc cay\n\n**Ví dụ:**\n- Bún bò Huế → Mình sẽ nhắc bỏ ớt, giảm mắm ruốc\n- Pad Thai → Bỏ ớt, chỉ dùng tiêu\n\nBạn còn sở thích gì khác không? (ít dầu, vegetarian...) 😊"
        },
        {
            "user": "Mình thích món Bắc hơn món Nam",
            "assistant": "Ghi nhớ rồi! ✅ Bạn thích món Bắc!\n\n**Sở thích của bạn:**\n⭐ Ưu tiên món miền Bắc\n\n**Từ giờ mình sẽ gợi ý:**\n🍜 Phở Hà Nội (không phải phở Nam)\n🍖 Bún chả\n🥟 Bánh cuốn Thanh Trì\n🍲 Chả cá Lã Vọng\n🍜 Bún thang\n\n**Đặc trưng món Bắc:**\n- Thanh đạm, nhẹ nhàng\n- Ít ngọt, ít cay\n- Chú trọng hương vị tự nhiên\n\nBạn còn sở thích gì nữa không? 😊"
        },
        {
            "user": "Gia đình mình ăn ít dầu mỡ",
            "assistant": "Đã ghi nhớ! ✅ Gia đình bạn ăn ít dầu mỡ!\n\n**Sở thích của bạn:**\n💚 Ít dầu mỡ\n\n**Mình sẽ điều chỉnh:**\n- Gợi ý món hấp, luộc thay chiên\n- Nhắc giảm dầu trong công thức\n- Đề xuất thay thế nguyên liệu\n\n**MÓN PHÙ HỢP:**\n✅ Cá hấp, gà luộc\n✅ Canh, súp\n✅ Salad, gỏi cuốn\n✅ Cơm trắng + món kho ít mỡ\n\n**MÓN NÊN HẠN CHẾ:**\n⚠️ Đồ chiên giòn\n⚠️ Thịt mỡ, da gà\n\nBạn cần gợi ý món healthy ngay không? 😊"
        },
    ]
    samples.extend(pref_qa)
    
    return samples

def generate_danger_detection():
    """11. Phát hiện yêu cầu nguy hiểm"""
    samples = []
    
    danger_qa = [
        {
            "user": "Con mình 2 tuổi, cho bé ăn sushi được không?",
            "assistant": "⚠️ **KHUYẾN CÁO AN TOÀN!**\n\n**KHÔNG NÊN** cho trẻ 2 tuổi ăn sushi có cá sống!\n\n**LÝ DO:**\n1. **Nguy cơ nhiễm khuẩn** - Hệ miễn dịch bé còn yếu\n2. **Ký sinh trùng** - Cá sống có thể chứa giun sán\n3. **Dị ứng** - Hải sản là allergen phổ biến ở trẻ\n4. **Nghẹn** - Miếng to, khó nhai\n\n**GIẢI PHÁP:**\n✅ Sushi rau củ (không cá)\n✅ Cá đã nấu chín (cá hồi nướng)\n✅ Cơm cuộn rong biển (không hải sản sống)\n\n**ĐỘ TUỔI AN TOÀN:**\n- Sushi cá sống: Từ 5-6 tuổi trở lên\n- Hải sản nấu chín: Từ 1 tuổi, thử từng ít\n\nBạn muốn mình gợi ý món phù hợp cho bé 2 tuổi không? 😊"
        },
        {
            "user": "Mình dị ứng tôm, công thức Pad Thai có tôm không?",
            "assistant": "⚠️ **CẢNH BÁO DỊ ỨNG!**\n\n**CÓ!** Pad Thai truyền thống **CÓ TÔM**!\n\n**KHÔNG AN TOÀN** cho bạn nếu dị ứng tôm.\n\n**THÀNH PHẦN NGUY HIỂM:**\n❌ Tôm tươi (topping)\n❌ Nước mắm (có thể chứa tôm/cá)\n❌ Mắm tôm (nếu có)\n\n**GIẢI PHÁP AN TOÀN:**\n\n**Pad Thai KHÔNG tôm:**\n1. Thay tôm bằng **gà** hoặc **đậu hủ**\n2. Dùng **nước tương** thay nước mắm\n3. Kiểm tra sauce có hải sản không\n\n**KHI ĂN NGOÀI:**\n- Thông báo nhà hàng về dị ứng\n- Hỏi chi tiết thành phần\n- Cẩn thận cross-contamination\n\nBạn muốn mình hướng dẫn Pad Thai an toàn không? 😊"
        },
        {
            "user": "Bà mình bị tiểu đường, cho bà ăn xoài chín được không?",
            "assistant": "⚠️ **LƯU Ý CHO NGƯỜI TIỂU ĐƯỜNG!**\n\nXoài chín có **chỉ số đường huyết CAO** (GI: 51-60) và nhiều đường tự nhiên.\n\n**KHUYẾN CÁO:**\n⚠️ **Hạn chế** ăn xoài chín, đặc biệt nếu đường huyết chưa ổn định.\n\n**NẾU MUỐN ĂN:**\n- Ăn **ít** (1-2 miếng nhỏ)\n- Ăn sau bữa chính (không ăn lúc đói)\n- Kiểm tra đường huyết sau 2 giờ\n- Xoài xanh tốt hơn xoài chín\n\n**TRÁI CÂY TỐT HƠN CHO TIỂU ĐƯỜNG:**\n✅ Táo (GI thấp)\n✅ Cam (ăn vừa phải)\n✅ Bưởi\n✅ Ổi\n✅ Dưa leo\n\n**TRÁI CÂY NÊN TRÁNH:**\n❌ Sầu riêng, mít, nhãn\n❌ Xoài chín, chuối chín\n\nBạn cần gợi ý thực đơn cho bà không? 😊"
        },
    ]
    samples.extend(danger_qa)
    
    return samples

def generate_explainability():
    """12. Giải thích vì sao gợi ý"""
    samples = []
    
    explain_qa = [
        {
            "user": "Sao bạn lại gợi ý món phở vậy?",
            "assistant": "Mình giải thích lý do gợi ý Phở nhé! 🤔\n\n**VÌ SAO MÌNH GỢI Ý PHỞ:**\n\n1. **Thời tiết hôm nay se lạnh** 🌡️\n   - Phở nóng hổi, ấm bụng\n   - Nước dùng xương hầm bổ dưỡng\n\n2. **Đầy đủ dinh dưỡng** 💪\n   - Protein: Thịt bò/gà\n   - Carb: Bánh phở\n   - Vitamin: Rau thơm, giá đỗ\n\n3. **Phù hợp bữa sáng/trưa** ⏰\n   - Dễ tiêu hóa\n   - No lâu, không quá nặng\n\n4. **Dễ điều chỉnh** ⚙️\n   - Ít/nhiều bánh tùy ý\n   - Thay đổi topping dễ dàng\n\n**Nếu bạn có sở thích khác**, cho mình biết nhé:\n- Không ăn bò? → Phở gà\n- Ăn chay? → Phở chay\n- Ít carb? → Nhiều rau, ít bánh\n\nBạn muốn thử món khác không? 😊"
        },
        {
            "user": "Vì sao bạn khuyên mình không nên ăn cơm chiên khi giảm cân?",
            "assistant": "Mình giải thích tại sao cơm chiên không tốt khi giảm cân nhé! 📊\n\n**LÝ DO KHÔNG NÊN:**\n\n1. **Calo CAO** 🔥\n   - 1 đĩa cơm chiên: ~600-800 calo\n   - Bằng 40-50% nhu cầu cả ngày!\n\n2. **Nhiều dầu mỡ** 🛢️\n   - Chiên với nhiều dầu\n   - Chất béo bão hòa cao\n\n3. **Carb tinh chế** 🍚\n   - Cơm trắng có GI cao\n   - Gây tăng đường huyết nhanh\n   - No nhanh nhưng mau đói\n\n4. **Ít rau, nhiều muối** 🧂\n   - Gây giữ nước\n   - Ít chất xơ\n\n**THAY THẾ TỐT HƠN:**\n✅ Cơm gạo lứt + rau xào\n✅ Salad + protein\n✅ Súp rau + thịt nạc\n\n**NẾU VẪN THÈM CƠM CHIÊN:**\n- Dùng cơm nguội (ít calo hơn)\n- Ít dầu, nhiều rau\n- Ăn 1/2 đĩa thôi\n\nBạn hiểu rồi chứ? 😊"
        },
        {
            "user": "Tại sao lại gợi ý lẩu cho ngày mưa?",
            "assistant": "Câu hỏi hay! Mình giải thích nhé! 🌧️🍲\n\n**VÌ SAO LẨU PHÙ HỢP NGÀY MƯA:**\n\n1. **Tâm lý** 🧠\n   - Trời mưa → cảm giác lạnh, cần ấm áp\n   - Lẩu nóng → tạo cảm giác ấm cúng\n   - Văn hóa Việt: \"Mưa thì ăn lẩu\"\n\n2. **Sinh lý** 🌡️\n   - Nhiệt độ giảm → cơ thể cần năng lượng\n   - Lẩu nóng → giữ ấm cơ thể\n   - Nước dùng → bù nước\n\n3. **Xã hội** 👨‍👩‍👧‍👦\n   - Mưa → ở nhà\n   - Lẩu → sum họp gia đình\n   - Ăn cùng nhau → vui hơn\n\n4. **Thực tế** 🍖\n   - Nhiều nguyên liệu → đa dạng\n   - Nấu tại bàn → tiện\n   - Ai cũng chọn được món thích\n\n**KHOA HỌC:**\n- Đồ ăn nóng kích thích vị giác\n- Tạo cảm giác thoải mái (comfort food)\n\nBạn muốn thử lẩu gì? Thái cay, gà lá é, hay hải sản? 😊"
        },
    ]
    samples.extend(explain_qa)
    
    return samples

# =============================================================================
# GREETINGS & GENERAL
# =============================================================================

def generate_greetings():
    """Câu chào hỏi"""
    samples = [
        {
            "user": "Xin chào",
            "assistant": "Chào bạn! 👋 Mình là CookBot, AI tư vấn món ăn của CookShare!\n\nMình có thể giúp bạn:\n🍳 Gợi ý món ăn theo nguyên liệu\n📝 Hướng dẫn nấu từng bước\n🔄 Thay thế nguyên liệu\n📅 Lên thực đơn tuần\n⚠️ Cảnh báo dị ứng\n\nBạn muốn mình giúp gì hôm nay? 😊"
        },
        {
            "user": "Hello",
            "assistant": "Hello! 👋 Mình là CookBot đây!\n\nMình sẵn sàng giúp bạn với mọi thứ về nấu ăn:\n- Công thức món Việt, món quốc tế\n- Gợi ý theo nguyên liệu có sẵn\n- Lên thực đơn, tính chi phí\n\nBạn đang muốn nấu món gì? 😊"
        },
        {
            "user": "Bạn là ai?",
            "assistant": "Mình là **CookBot** - AI tư vấn món ăn của ứng dụng **CookShare**! 🤖👨‍🍳\n\n**Mình có thể giúp bạn:**\n- 🍳 Gợi ý công thức từ nguyên liệu\n- 📝 Hướng dẫn nấu từng bước chi tiết\n- 🔄 Thay thế nguyên liệu khi thiếu\n- 📅 Lên thực đơn ngày/tuần\n- ⚠️ Cảnh báo dị ứng, kiêng kỵ\n- 💰 Ước tính chi phí nấu ăn\n\nHỏi mình bất cứ điều gì về nấu ăn nhé! 😊"
        },
        {
            "user": "Hôm nay mình đói quá",
            "assistant": "Đói rồi à! 😋 Để mình gợi ý nhanh!\n\n**Món nhanh (10-15 phút):**\n1. Mì xào trứng rau\n2. Cơm chiên\n3. Trứng chiên + cơm\n\n**Món vừa (20-30 phút):**\n1. Bún thịt nướng\n2. Cơm tấm sườn\n3. Phở (nếu có sẵn nước dùng)\n\n**Order ngoài:**\n- Grab Food, ShopeeFood 📱\n\nBạn có nguyên liệu gì trong tủ lạnh? Mình gợi ý cụ thể hơn! 😊"
        },
        {
            "user": "Cảm ơn bạn",
            "assistant": "Không có gì! 😊 Rất vui được giúp bạn!\n\nNếu cần thêm gợi ý hay công thức gì, cứ hỏi mình nhé!\n\nChúc bạn nấu ăn ngon miệng! 🍳👨‍🍳"
        },
    ]
    return samples

# =============================================================================
# MAIN GENERATOR
# =============================================================================

def generate_all():
    """Generate tất cả samples và save vào files"""
    all_samples = []
    
    print("🚀 Bắt đầu generate dataset...")
    
    # Greetings
    greetings = generate_greetings()
    save_jsonl(greetings, "dataset/greetings.jsonl")
    all_samples.extend(greetings)
    
    # Tầng 1: Core
    print("\n📦 Tầng 1: Core Features")
    
    ingredients = generate_ingredients_to_recipe()
    save_jsonl(ingredients, "dataset/01_core/ingredients_to_recipe.jsonl")
    all_samples.extend(ingredients)
    
    steps = generate_step_by_step()
    save_jsonl(steps, "dataset/01_core/step_by_step.jsonl")
    all_samples.extend(steps)
    
    subs = generate_substitutions()
    save_jsonl(subs, "dataset/01_core/substitutions.jsonl")
    all_samples.extend(subs)
    
    portions = generate_portion_scaling()
    save_jsonl(portions, "dataset/01_core/portions.jsonl")
    all_samples.extend(portions)
    
    allergies = generate_allergy_warnings()
    save_jsonl(allergies, "dataset/01_core/allergies.jsonl")
    all_samples.extend(allergies)
    
    # Tầng 2: Advanced
    print("\n📦 Tầng 2: Advanced Features")
    
    meals = generate_meal_planning()
    save_jsonl(meals, "dataset/02_advanced/meal_planning.jsonl")
    all_samples.extend(meals)
    
    weather = generate_weather_suggestions()
    save_jsonl(weather, "dataset/02_advanced/weather.jsonl")
    all_samples.extend(weather)
    
    shopping = generate_shopping_list()
    save_jsonl(shopping, "dataset/02_advanced/shopping.jsonl")
    all_samples.extend(shopping)
    
    costs = generate_cost_estimation()
    save_jsonl(costs, "dataset/02_advanced/costs.jsonl")
    all_samples.extend(costs)
    
    # Tầng 3: AI Features
    print("\n📦 Tầng 3: AI Features")
    
    prefs = generate_user_preferences()
    save_jsonl(prefs, "dataset/03_ai_features/preferences.jsonl")
    all_samples.extend(prefs)
    
    danger = generate_danger_detection()
    save_jsonl(danger, "dataset/03_ai_features/danger_detection.jsonl")
    all_samples.extend(danger)
    
    explain = generate_explainability()
    save_jsonl(explain, "dataset/03_ai_features/explainability.jsonl")
    all_samples.extend(explain)
    
    # Save all to train.jsonl
    print("\n💾 Saving combined train.jsonl...")
    save_jsonl(all_samples, "dataset/train.jsonl")
    
    print(f"\n✅ HOÀN THÀNH! Tổng cộng: {len(all_samples)} samples")
    return all_samples

if __name__ == "__main__":
    generate_all()

