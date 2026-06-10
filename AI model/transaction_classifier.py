# transaction_classifier.py

from ai_providers import ask_qwen, ask_phi
from parallel_ai import run_parallel_ai


CATEGORIES = [
    "Ăn uống",
    "Di chuyển",
    "Học tập",
    "Nhà ở",
    "Mua sắm",
    "Giải trí",
    "Sức khỏe",
    "Thu nhập",
    "Khác"
]


def classify_by_rule(description: str, trans_type: str) -> str:
    text = description.lower()

    if trans_type == "Thu":
        return "Thu nhập"

    food_keywords = [
        "ăn", "cơm", "bún", "phở", "trà sữa", "cà phê",
        "cafe", "nước", "buffet", "bánh", "mì"
    ]

    transport_keywords = [
        "xăng", "grab", "taxi", "xe", "bus",
        "vé xe", "đi lại", "gửi xe"
    ]

    study_keywords = [
        "sách", "vở", "học", "khóa học",
        "bút", "tài liệu", "học phí"
    ]

    house_keywords = [
        "trọ", "nhà", "điện", "nước",
        "wifi", "internet", "phòng", "tiền phòng"
    ]

    shopping_keywords = [
        "áo", "quần", "giày", "mua",
        "shopee", "lazada", "tiki", "túi"
    ]

    entertainment_keywords = [
        "phim", "game", "karaoke", "du lịch", "giải trí"
    ]

    health_keywords = [
        "thuốc", "bệnh", "khám", "bác sĩ", "vitamin", "y tế"
    ]

    if any(word in text for word in food_keywords):
        return "Ăn uống"

    if any(word in text for word in transport_keywords):
        return "Di chuyển"

    if any(word in text for word in study_keywords):
        return "Học tập"

    if any(word in text for word in house_keywords):
        return "Nhà ở"

    if any(word in text for word in shopping_keywords):
        return "Mua sắm"

    if any(word in text for word in entertainment_keywords):
        return "Giải trí"

    if any(word in text for word in health_keywords):
        return "Sức khỏe"

    return "Khác"


def classify_transaction(description: str, trans_type: str) -> str:
    rule_category = classify_by_rule(description, trans_type)

    if rule_category != "Khác":
        return rule_category

    prompt = f"""
Phân loại giao dịch sau vào đúng một danh mục.

Mô tả: {description}
Loại: {trans_type}

Danh mục hợp lệ:
{", ".join(CATEGORIES)}

Chỉ trả về đúng một danh mục. Không giải thích.
"""

    ai_results = run_parallel_ai(
        {
            "Qwen AI": ask_qwen,
            "Phi AI": ask_phi
        },
        prompt
    )

    for _, answer in ai_results.items():
        for category in CATEGORIES:
            if category.lower() in answer.lower():
                return category

    return "Khác"