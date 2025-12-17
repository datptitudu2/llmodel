"""
CookBot Recipes Database
Database công thức thật với đầy đủ thông tin
"""

# =============================================================================
# MÓN BẮC
# =============================================================================
MON_BAC = {
    "pho_bo": {
        "name": "Phở Bò",
        "region": "Bắc",
        "time": "3 giờ",
        "difficulty": "Trung bình",
        "servings": 4,
        "calories": 450,
        "ingredients": {
            "xương_bò": {"amount": 1, "unit": "kg", "price": 80000},
            "thịt_bò_tái": {"amount": 300, "unit": "g", "price": 120000},
            "bánh_phở": {"amount": 500, "unit": "g", "price": 25000},
            "hành_tây": {"amount": 2, "unit": "củ", "price": 10000},
            "gừng": {"amount": 1, "unit": "củ", "price": 5000},
            "quế": {"amount": 2, "unit": "thanh", "price": 3000},
            "hồi": {"amount": 3, "unit": "cánh", "price": 3000},
            "hành_lá": {"amount": 1, "unit": "bó", "price": 5000},
            "ngò_gai": {"amount": 1, "unit": "bó", "price": 5000},
            "giá_đỗ": {"amount": 200, "unit": "g", "price": 10000},
            "nước_mắm": {"amount": 3, "unit": "muỗng", "price": 5000},
        },
        "steps": [
            "Rửa sạch xương bò, chần qua nước sôi để loại bỏ bọt bẩn",
            "Nướng hành tây và gừng trên bếp cho cháy xém vỏ ngoài",
            "Cho xương vào nồi lớn, đổ 4 lít nước, đun sôi rồi hạ lửa nhỏ",
            "Thêm hành tây, gừng, quế, hồi. Ninh lửa nhỏ 2-3 giờ",
            "Vớt bọt thường xuyên trong quá trình ninh",
            "Nêm nước mắm, muối cho vừa miệng",
            "Thái thịt bò thật mỏng",
            "Trần bánh phở qua nước sôi 30 giây, cho vào tô",
            "Xếp thịt bò tái lên, chan nước dùng nóng già",
            "Thêm hành lá, ngò gai, giá đỗ. Ăn kèm chanh, ớt"
        ],
        "tips": [
            "Nước dùng phải trong, ngọt tự nhiên từ xương",
            "Ninh lửa nhỏ để nước không bị đục",
            "Thịt lạnh sẽ dễ thái mỏng hơn"
        ],
        "allergens": ["gluten"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "bánh_phở": ["bún tươi", "mì gạo"],
            "thịt_bò": ["gà", "heo"],
        }
    },
    
    "bun_cha": {
        "name": "Bún Chả Hà Nội",
        "region": "Bắc",
        "time": "1 giờ",
        "difficulty": "Dễ",
        "servings": 4,
        "calories": 520,
        "ingredients": {
            "thịt_ba_chỉ": {"amount": 300, "unit": "g", "price": 90000},
            "thịt_nạc_vai": {"amount": 300, "unit": "g", "price": 85000},
            "bún_tươi": {"amount": 500, "unit": "g", "price": 20000},
            "nước_mắm": {"amount": 100, "unit": "ml", "price": 15000},
            "đường": {"amount": 80, "unit": "g", "price": 5000},
            "tỏi": {"amount": 5, "unit": "tép", "price": 5000},
            "giấm": {"amount": 50, "unit": "ml", "price": 5000},
            "rau_sống": {"amount": 200, "unit": "g", "price": 15000},
        },
        "steps": [
            "Thái thịt ba chỉ miếng mỏng, thịt nạc băm nhỏ vo viên",
            "Ướp thịt với nước mắm, đường, tỏi băm 30 phút",
            "Làm nước chấm: nước mắm + đường + giấm + nước ấm",
            "Thêm tỏi ớt băm vào nước chấm",
            "Nướng thịt trên than hoa đến khi vàng thơm",
            "Cho thịt nướng vào bát nước chấm",
            "Bày bún ra đĩa, ăn kèm rau sống"
        ],
        "tips": [
            "Ướp thịt qua đêm sẽ ngon hơn",
            "Nướng than hoa mới đúng vị Hà Nội"
        ],
        "allergens": ["gluten"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "thịt_ba_chỉ": ["thịt nạc vai", "thịt gà"],
            "bún_tươi": ["bánh phở", "miến"],
        }
    },
    
    "banh_cuon": {
        "name": "Bánh Cuốn Thanh Trì",
        "region": "Bắc",
        "time": "1.5 giờ",
        "difficulty": "Khó",
        "servings": 4,
        "calories": 320,
        "ingredients": {
            "bột_gạo": {"amount": 300, "unit": "g", "price": 20000},
            "thịt_heo_xay": {"amount": 200, "unit": "g", "price": 60000},
            "mộc_nhĩ": {"amount": 50, "unit": "g", "price": 15000},
            "hành_khô": {"amount": 100, "unit": "g", "price": 20000},
            "chả_lụa": {"amount": 100, "unit": "g", "price": 30000},
            "nước_mắm": {"amount": 50, "unit": "ml", "price": 10000},
        },
        "steps": [
            "Pha bột gạo với nước theo tỷ lệ 1:2, để nghỉ 2 giờ",
            "Ngâm mộc nhĩ, băm nhỏ. Phi thơm hành khô",
            "Xào thịt xay với mộc nhĩ, hành phi, nêm gia vị",
            "Tráng bánh trên vải mỏng căng trên nồi hấp",
            "Đổ một lớp bột mỏng, đậy nắp 30 giây",
            "Gỡ bánh ra, cho nhân vào cuốn lại",
            "Ăn kèm chả lụa, hành phi, nước mắm pha"
        ],
        "tips": [
            "Bột phải mịn, không vón cục",
            "Tráng bánh thật mỏng mới ngon"
        ],
        "allergens": ["gluten"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "thịt_heo": ["tôm", "nấm (chay)"],
        }
    },
}

# =============================================================================
# MÓN TRUNG
# =============================================================================
MON_TRUNG = {
    "bun_bo_hue": {
        "name": "Bún Bò Huế",
        "region": "Trung",
        "time": "3 giờ",
        "difficulty": "Khó",
        "servings": 6,
        "calories": 580,
        "ingredients": {
            "xương_bò": {"amount": 1, "unit": "kg", "price": 80000},
            "bắp_bò": {"amount": 500, "unit": "g", "price": 150000},
            "giò_heo": {"amount": 2, "unit": "cái", "price": 80000},
            "chả_cua": {"amount": 200, "unit": "g", "price": 60000},
            "bún_tươi": {"amount": 1, "unit": "kg", "price": 30000},
            "sả": {"amount": 5, "unit": "cây", "price": 10000},
            "ớt_bột": {"amount": 3, "unit": "muỗng", "price": 10000},
            "mắm_ruốc": {"amount": 2, "unit": "muỗng", "price": 15000},
            "rau_muống": {"amount": 300, "unit": "g", "price": 10000},
            "bắp_chuối": {"amount": 1, "unit": "bắp", "price": 15000},
        },
        "steps": [
            "Rửa sạch xương, bắp bò, giò heo. Chần qua nước sôi",
            "Đập dập sả, cho vào nồi cùng xương. Đổ 5 lít nước",
            "Hạ lửa nhỏ, ninh 2 giờ. Vớt bọt thường xuyên",
            "Phi dầu với ớt bột tạo màu đỏ đẹp",
            "Hòa mắm ruốc với nước dùng, lọc bỏ cặn",
            "Vớt bắp bò, giò heo khi chín, thái miếng",
            "Nêm nước mắm, muối, đường. Thêm dầu ớt",
            "Trần bún, cho vào tô. Xếp thịt, chả cua",
            "Chan nước dùng nóng, thêm rau"
        ],
        "tips": [
            "Mắm ruốc tạo vị đặc trưng Huế",
            "Bún bò Huế phải cay mới đúng vị"
        ],
        "allergens": ["gluten", "shellfish"],
        "dietary": ["cay", "không phù hợp vegetarian"],
        "substitutions": {
            "mắm_ruốc": ["mắm tôm pha loãng"],
            "chả_cua": ["chả lụa"],
        }
    },
    
    "mi_quang": {
        "name": "Mì Quảng",
        "region": "Trung",
        "time": "1.5 giờ",
        "difficulty": "Trung bình",
        "servings": 4,
        "calories": 480,
        "ingredients": {
            "mì_quảng": {"amount": 500, "unit": "g", "price": 30000},
            "thịt_gà": {"amount": 300, "unit": "g", "price": 80000},
            "tôm": {"amount": 200, "unit": "g", "price": 100000},
            "trứng_cút": {"amount": 12, "unit": "quả", "price": 25000},
            "đậu_phộng": {"amount": 100, "unit": "g", "price": 20000},
            "bánh_tráng": {"amount": 10, "unit": "cái", "price": 15000},
            "nghệ": {"amount": 1, "unit": "củ", "price": 5000},
            "rau_sống": {"amount": 200, "unit": "g", "price": 15000},
        },
        "steps": [
            "Luộc gà chín, xé sợi. Giữ nước luộc",
            "Làm sạch tôm, ướp muối tiêu",
            "Phi hành với nghệ tạo màu vàng",
            "Xào tôm chín, múc ra",
            "Cho nước luộc gà vào nồi, nêm gia vị",
            "Luộc trứng cút, bóc vỏ",
            "Rang đậu phộng, giã dập",
            "Cho mì vào tô, xếp gà, tôm, trứng",
            "Chan ít nước dùng, rắc đậu phộng"
        ],
        "tips": [
            "Mì Quảng ăn ít nước, không như phở",
            "Bánh tráng bẻ vụn ăn kèm"
        ],
        "allergens": ["gluten", "peanuts", "shellfish", "eggs"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "tôm": ["thịt heo"],
            "đậu_phộng": ["hạt điều"],
        }
    },
    
    "banh_xeo": {
        "name": "Bánh Xèo Miền Trung",
        "region": "Trung",
        "time": "45 phút",
        "difficulty": "Trung bình",
        "servings": 4,
        "calories": 380,
        "ingredients": {
            "bột_gạo": {"amount": 200, "unit": "g", "price": 15000},
            "bột_nghệ": {"amount": 1, "unit": "muỗng", "price": 5000},
            "nước_cốt_dừa": {"amount": 200, "unit": "ml", "price": 20000},
            "tôm": {"amount": 200, "unit": "g", "price": 100000},
            "thịt_ba_chỉ": {"amount": 150, "unit": "g", "price": 50000},
            "giá_đỗ": {"amount": 200, "unit": "g", "price": 10000},
            "hành_lá": {"amount": 1, "unit": "bó", "price": 5000},
            "rau_sống": {"amount": 300, "unit": "g", "price": 20000},
        },
        "steps": [
            "Pha bột gạo với nước cốt dừa, nghệ, chút muối",
            "Để bột nghỉ 30 phút",
            "Thái thịt ba chỉ mỏng, làm sạch tôm",
            "Đun nóng chảo, cho dầu",
            "Cho thịt, tôm vào xào sơ",
            "Đổ bột vào, tráng đều, đậy nắp",
            "Cho giá đỗ vào, gấp đôi bánh",
            "Chiên giòn, ăn kèm rau sống, nước mắm"
        ],
        "tips": [
            "Chảo phải thật nóng bánh mới giòn",
            "Nước cốt dừa làm bánh thơm béo"
        ],
        "allergens": ["shellfish", "gluten"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "tôm": ["mực", "nấm"],
            "nước_cốt_dừa": ["nước thường"],
        }
    },
}

# =============================================================================
# MÓN NAM
# =============================================================================
MON_NAM = {
    "com_tam": {
        "name": "Cơm Tấm Sườn Bì Chả",
        "region": "Nam",
        "time": "1 giờ",
        "difficulty": "Trung bình",
        "servings": 4,
        "calories": 650,
        "ingredients": {
            "gạo_tấm": {"amount": 400, "unit": "g", "price": 25000},
            "sườn_heo": {"amount": 4, "unit": "miếng", "price": 100000},
            "bì_heo": {"amount": 200, "unit": "g", "price": 40000},
            "trứng": {"amount": 4, "unit": "quả", "price": 20000},
            "mỡ_hành": {"amount": 50, "unit": "ml", "price": 10000},
            "đồ_chua": {"amount": 200, "unit": "g", "price": 15000},
            "nước_mắm": {"amount": 100, "unit": "ml", "price": 15000},
            "sả": {"amount": 2, "unit": "cây", "price": 5000},
        },
        "steps": [
            "Vo gạo tấm, ngâm 30 phút. Nấu cơm tỷ lệ 1:1",
            "Ướp sườn với sả, tỏi, nước mắm, đường 1 giờ",
            "Nướng sườn vàng đều hoặc chiên áp chảo",
            "Luộc bì heo, thái sợi, trộn thính",
            "Làm chả: băm thịt, trộn trứng, hấp 20 phút",
            "Chiên trứng ốp la lòng đào",
            "Pha nước mắm: mắm + đường + nước + tỏi ớt",
            "Xới cơm, xếp sườn, bì, chả, trứng lên",
            "Rưới mỡ hành, ăn kèm đồ chua"
        ],
        "tips": [
            "Gạo tấm cần ít nước hơn gạo thường",
            "Sườn nướng than thơm hơn chiên"
        ],
        "allergens": ["eggs", "gluten"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "sườn_heo": ["sườn gà"],
            "gạo_tấm": ["gạo thường"],
        }
    },
    
    "hu_tieu": {
        "name": "Hủ Tiếu Nam Vang",
        "region": "Nam",
        "time": "2 giờ",
        "difficulty": "Trung bình",
        "servings": 4,
        "calories": 420,
        "ingredients": {
            "hủ_tiếu": {"amount": 400, "unit": "g", "price": 25000},
            "xương_heo": {"amount": 500, "unit": "g", "price": 50000},
            "thịt_băm": {"amount": 200, "unit": "g", "price": 60000},
            "gan_heo": {"amount": 150, "unit": "g", "price": 40000},
            "tôm": {"amount": 200, "unit": "g", "price": 100000},
            "trứng_cút": {"amount": 12, "unit": "quả", "price": 25000},
            "hành_phi": {"amount": 50, "unit": "g", "price": 20000},
            "cần_tây": {"amount": 100, "unit": "g", "price": 15000},
        },
        "steps": [
            "Ninh xương heo 2 giờ, lửa nhỏ",
            "Vo viên thịt băm, luộc trong nước dùng",
            "Thái gan mỏng, trần qua nước sôi",
            "Làm sạch tôm, luộc chín",
            "Luộc trứng cút, bóc vỏ",
            "Nêm nước dùng với nước mắm, muối",
            "Trần hủ tiếu, cho vào tô",
            "Xếp thịt, gan, tôm, trứng lên",
            "Chan nước dùng, rắc hành phi, cần tây"
        ],
        "tips": [
            "Nước dùng phải trong và ngọt tự nhiên",
            "Hủ tiếu dai, không trần lâu"
        ],
        "allergens": ["shellfish", "gluten"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "gan_heo": ["thịt nạc"],
            "hủ_tiếu": ["mì", "bún"],
        }
    },
    
    "canh_chua": {
        "name": "Canh Chua Cá Lóc",
        "region": "Nam",
        "time": "45 phút",
        "difficulty": "Trung bình",
        "servings": 4,
        "calories": 180,
        "ingredients": {
            "cá_lóc": {"amount": 500, "unit": "g", "price": 80000},
            "me": {"amount": 50, "unit": "g", "price": 10000},
            "thơm": {"amount": 1, "unit": "quả", "price": 20000},
            "cà_chua": {"amount": 3, "unit": "quả", "price": 15000},
            "bạc_hà": {"amount": 200, "unit": "g", "price": 15000},
            "giá_đỗ": {"amount": 200, "unit": "g", "price": 10000},
            "đậu_bắp": {"amount": 100, "unit": "g", "price": 15000},
            "ngò_gai": {"amount": 1, "unit": "bó", "price": 5000},
        },
        "steps": [
            "Làm sạch cá, cắt khúc, ướp muối tiêu",
            "Ngâm me với nước ấm, vắt lấy nước chua",
            "Cắt thơm, cà chua, bạc hà",
            "Đun sôi nước, cho thơm vào nấu trước",
            "Cho nước me, cà chua, nêm gia vị",
            "Cho cá vào khi nước sôi, nấu 5-7 phút",
            "Cho bạc hà, đậu bắp, giá đỗ. Tắt bếp",
            "Rắc ngò gai, ớt. Ăn nóng với cơm"
        ],
        "tips": [
            "Cá rửa với gừng để khử tanh",
            "Rau cho sau cùng để giữ giòn"
        ],
        "allergens": ["fish"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "cá_lóc": ["cá basa", "cá tra"],
            "me": ["chanh", "khế chua"],
        }
    },
}

# =============================================================================
# MÓN CHAY
# =============================================================================
MON_CHAY = {
    "pho_chay": {
        "name": "Phở Chay",
        "region": "Việt Nam",
        "time": "1 giờ",
        "difficulty": "Dễ",
        "servings": 4,
        "calories": 280,
        "ingredients": {
            "bánh_phở": {"amount": 500, "unit": "g", "price": 25000},
            "đậu_hủ": {"amount": 300, "unit": "g", "price": 15000},
            "nấm_đông_cô": {"amount": 100, "unit": "g", "price": 30000},
            "nấm_rơm": {"amount": 100, "unit": "g", "price": 25000},
            "cà_rốt": {"amount": 2, "unit": "củ", "price": 10000},
            "củ_cải_trắng": {"amount": 1, "unit": "củ", "price": 10000},
            "nước_tương": {"amount": 3, "unit": "muỗng", "price": 10000},
        },
        "steps": [
            "Nướng hành tây, gừng cho thơm",
            "Nấu nước dùng với củ cải, cà rốt 45 phút",
            "Ngâm nấm, thái miếng, xào sơ",
            "Chiên đậu hủ vàng đều",
            "Nêm nước dùng với nước tương",
            "Trần bánh phở, cho vào tô",
            "Xếp đậu hủ, nấm, chan nước dùng",
            "Thêm rau thơm, giá đỗ"
        ],
        "tips": [
            "Rau củ tạo vị ngọt tự nhiên",
            "Nấm đông cô cho nước dùng thơm"
        ],
        "allergens": ["gluten", "soy"],
        "dietary": ["vegetarian", "vegan"],
        "substitutions": {
            "đậu_hủ": ["đậu hủ ki"],
            "nấm_đông_cô": ["nấm hương"],
        }
    },
    
    "com_chay": {
        "name": "Cơm Chay Thập Cẩm",
        "region": "Việt Nam",
        "time": "45 phút",
        "difficulty": "Dễ",
        "servings": 2,
        "calories": 350,
        "ingredients": {
            "cơm": {"amount": 2, "unit": "chén", "price": 10000},
            "đậu_hủ": {"amount": 200, "unit": "g", "price": 12000},
            "nấm_các_loại": {"amount": 150, "unit": "g", "price": 25000},
            "rau_củ": {"amount": 200, "unit": "g", "price": 15000},
            "nước_tương": {"amount": 2, "unit": "muỗng", "price": 5000},
        },
        "steps": [
            "Chiên đậu hủ vàng giòn",
            "Xào nấm với chút dầu và nước tương",
            "Xào rau củ (cà rốt, đậu que, bông cải)",
            "Nêm gia vị với nước tương, tiêu",
            "Xới cơm ra đĩa",
            "Bày đậu hủ, nấm, rau củ lên trên"
        ],
        "tips": [
            "Đậu hủ ráo nước sẽ chiên giòn",
            "Rau củ xào lửa lớn để giữ giòn"
        ],
        "allergens": ["soy", "gluten"],
        "dietary": ["vegetarian", "vegan"],
        "substitutions": {
            "đậu_hủ": ["tempeh", "seitan"],
        }
    },
}

# =============================================================================
# MÓN QUỐC TẾ
# =============================================================================
MON_QUOC_TE = {
    "pasta_carbonara": {
        "name": "Pasta Carbonara",
        "region": "Ý",
        "time": "30 phút",
        "difficulty": "Trung bình",
        "servings": 2,
        "calories": 550,
        "ingredients": {
            "spaghetti": {"amount": 200, "unit": "g", "price": 35000},
            "bacon": {"amount": 150, "unit": "g", "price": 60000},
            "trứng": {"amount": 3, "unit": "quả", "price": 15000},
            "parmesan": {"amount": 80, "unit": "g", "price": 50000},
            "tỏi": {"amount": 2, "unit": "tép", "price": 3000},
            "tiêu_đen": {"amount": 1, "unit": "muỗng", "price": 5000},
        },
        "steps": [
            "Luộc spaghetti trong nước muối",
            "Đánh trứng với parmesan bào, tiêu đen",
            "Chiên bacon giòn, vớt ra",
            "Phi thơm tỏi trong mỡ bacon",
            "Cho mì vào chảo, TẮT BẾP",
            "Đổ hỗn hợp trứng vào, đảo nhanh",
            "Thêm nước luộc mì nếu khô",
            "Rắc bacon, parmesan, tiêu"
        ],
        "tips": [
            "PHẢI tắt bếp trước khi cho trứng",
            "Nước luộc mì giúp sauce sánh"
        ],
        "allergens": ["gluten", "eggs", "dairy"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "bacon": ["pancetta", "nấm (vegetarian)"],
            "parmesan": ["pecorino romano"],
        }
    },
    
    "pad_thai": {
        "name": "Pad Thai",
        "region": "Thái Lan",
        "time": "30 phút",
        "difficulty": "Trung bình",
        "servings": 2,
        "calories": 450,
        "ingredients": {
            "phở_khô": {"amount": 200, "unit": "g", "price": 25000},
            "tôm": {"amount": 150, "unit": "g", "price": 80000},
            "đậu_hủ": {"amount": 100, "unit": "g", "price": 10000},
            "trứng": {"amount": 2, "unit": "quả", "price": 10000},
            "giá_đỗ": {"amount": 100, "unit": "g", "price": 8000},
            "đậu_phộng": {"amount": 50, "unit": "g", "price": 15000},
            "nước_mắm": {"amount": 2, "unit": "muỗng", "price": 5000},
            "đường_thốt_nốt": {"amount": 2, "unit": "muỗng", "price": 10000},
            "me": {"amount": 2, "unit": "muỗng", "price": 8000},
        },
        "steps": [
            "Ngâm phở khô trong nước ấm 30 phút",
            "Pha sauce: nước mắm + đường thốt nốt + me",
            "Chiên đậu hủ vàng, để riêng",
            "Xào tôm chín, để riêng",
            "Đập trứng vào chảo, đảo nhanh",
            "Cho phở vào, thêm sauce, đảo đều",
            "Thêm tôm, đậu hủ, giá đỗ",
            "Rắc đậu phộng rang, chanh, ớt"
        ],
        "tips": [
            "Phở không ngâm quá lâu sẽ bị nát",
            "Sauce phải cân bằng chua ngọt mặn"
        ],
        "allergens": ["shellfish", "peanuts", "eggs", "soy"],
        "dietary": ["không phù hợp vegetarian (có tôm)"],
        "substitutions": {
            "tôm": ["gà", "đậu hủ (vegetarian)"],
            "đậu_phộng": ["hạt điều"],
        }
    },
    
    "kimchi_jjigae": {
        "name": "Canh Kim Chi (Kimchi Jjigae)",
        "region": "Hàn Quốc",
        "time": "40 phút",
        "difficulty": "Dễ",
        "servings": 2,
        "calories": 320,
        "ingredients": {
            "kim_chi": {"amount": 200, "unit": "g", "price": 40000},
            "thịt_ba_chỉ": {"amount": 150, "unit": "g", "price": 50000},
            "đậu_hủ": {"amount": 200, "unit": "g", "price": 12000},
            "hành_lá": {"amount": 2, "unit": "cọng", "price": 3000},
            "tỏi": {"amount": 3, "unit": "tép", "price": 3000},
            "gochugaru": {"amount": 1, "unit": "muỗng", "price": 15000},
        },
        "steps": [
            "Thái thịt ba chỉ miếng vừa",
            "Xào thịt với kim chi 5 phút",
            "Đổ nước vào, đun sôi",
            "Thêm tỏi băm, gochugaru",
            "Nấu 15 phút cho ngấm",
            "Cho đậu hủ cắt khối vào",
            "Nấu thêm 5 phút",
            "Rắc hành lá, ăn nóng với cơm"
        ],
        "tips": [
            "Kim chi cũ sẽ ngon hơn kim chi mới",
            "Ăn nóng với cơm trắng"
        ],
        "allergens": ["soy"],
        "dietary": ["cay", "không phù hợp vegetarian"],
        "substitutions": {
            "thịt_ba_chỉ": ["cá ngừ", "đậu hủ (vegetarian)"],
        }
    },
}

# =============================================================================
# MÓN ĂN NHANH / ĐƠN GIẢN
# =============================================================================
MON_NHANH = {
    "trung_chien": {
        "name": "Trứng Chiên",
        "region": "Việt Nam",
        "time": "10 phút",
        "difficulty": "Dễ",
        "servings": 1,
        "calories": 180,
        "ingredients": {
            "trứng": {"amount": 2, "unit": "quả", "price": 10000},
            "hành_lá": {"amount": 1, "unit": "cọng", "price": 2000},
            "dầu_ăn": {"amount": 2, "unit": "muỗng", "price": 3000},
            "nước_mắm": {"amount": 1, "unit": "muỗng", "price": 2000},
        },
        "steps": [
            "Đập trứng, thêm nước mắm, tiêu, đánh tan",
            "Thái hành lá, cho vào trứng",
            "Đun nóng chảo, cho dầu",
            "Đổ trứng vào khi dầu nóng",
            "Chiên lửa vừa, lật mặt khi vàng"
        ],
        "tips": [
            "Thêm 1 muỗng nước để trứng mềm",
            "Dầu nóng già trứng sẽ xốp"
        ],
        "allergens": ["eggs"],
        "dietary": ["vegetarian"],
        "substitutions": {
            "trứng_gà": ["trứng vịt", "trứng cút"],
        }
    },
    
    "mi_xao": {
        "name": "Mì Xào Thập Cẩm",
        "region": "Việt Nam",
        "time": "20 phút",
        "difficulty": "Dễ",
        "servings": 2,
        "calories": 420,
        "ingredients": {
            "mì_trứng": {"amount": 200, "unit": "g", "price": 20000},
            "thịt_heo": {"amount": 100, "unit": "g", "price": 35000},
            "tôm": {"amount": 100, "unit": "g", "price": 50000},
            "rau_củ": {"amount": 200, "unit": "g", "price": 20000},
            "nước_tương": {"amount": 2, "unit": "muỗng", "price": 5000},
            "dầu_hào": {"amount": 1, "unit": "muỗng", "price": 5000},
        },
        "steps": [
            "Luộc mì sơ, để ráo",
            "Thái thịt mỏng, làm sạch tôm",
            "Cắt rau củ: cà rốt, bắp cải, đậu que",
            "Xào thịt, tôm chín, để riêng",
            "Xào rau củ với chút dầu",
            "Cho mì vào, thêm nước tương, dầu hào",
            "Đảo đều, cho thịt tôm vào",
            "Nêm gia vị, rắc tiêu"
        ],
        "tips": [
            "Xào lửa lớn để rau giòn",
            "Mì không luộc quá chín"
        ],
        "allergens": ["gluten", "shellfish", "soy"],
        "dietary": ["không phù hợp vegetarian"],
        "substitutions": {
            "mì_trứng": ["mì gạo", "bún"],
            "tôm": ["mực", "bỏ qua"],
        }
    },
}

# =============================================================================
# TẤT CẢ CÔNG THỨC
# =============================================================================
ALL_RECIPES = {
    **MON_BAC,
    **MON_TRUNG,
    **MON_NAM,
    **MON_CHAY,
    **MON_QUOC_TE,
    **MON_NHANH,
}

# Danh sách nguyên liệu phổ biến
COMMON_INGREDIENTS = [
    "trứng", "thịt heo", "thịt bò", "thịt gà", "tôm", "cá",
    "đậu hủ", "nấm", "rau củ", "cà chua", "hành", "tỏi",
    "gừng", "ớt", "nước mắm", "nước tương", "muối", "đường",
    "dầu ăn", "tiêu", "bún", "phở", "mì", "cơm"
]

# Dị ứng phổ biến
COMMON_ALLERGENS = {
    "gluten": ["bún", "phở", "mì", "bánh mì", "bánh"],
    "shellfish": ["tôm", "cua", "mực", "nghêu", "sò", "ốc"],
    "eggs": ["trứng"],
    "dairy": ["sữa", "bơ", "phô mai", "kem"],
    "peanuts": ["đậu phộng", "lạc"],
    "soy": ["đậu nành", "đậu hủ", "nước tương", "tương"],
    "fish": ["cá", "nước mắm"],
}

# Chế độ ăn
DIETARY_RESTRICTIONS = {
    "vegetarian": "Không thịt, cá",
    "vegan": "Không thịt, cá, trứng, sữa",
    "halal": "Không thịt heo",
    "low_carb": "Ít tinh bột",
    "low_sodium": "Ít muối",
    "diabetic": "Ít đường, chỉ số đường huyết thấp",
}

