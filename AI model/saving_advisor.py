# saving_advisor.py

import re
from datetime import datetime

from database import get_finance_summary_text, get_monthly_summary
from ai_providers import ask_llama, ask_mistral, ask_gemma, ask_deepseek
from parallel_ai import run_parallel_ai, combine_answers_to_one


def extract_month(question: str):
    text = question.lower()

    match = re.search(r"tháng\s*(\d{1,2})", text)

    if match:
        month = int(match.group(1))
        if 1 <= month <= 12:
            return month

    return datetime.now().month


def answer_fast_finance_question(user_question: str):
    text = user_question.lower()
    current_year = datetime.now().year
    month = extract_month(text)

    monthly = get_monthly_summary(month, current_year)

    if "thu nhập" in text or "tổng thu" in text:
        return (
            f"Thu nhập tháng {month}/{current_year} của bạn là "
            f"{monthly['total_income']:,.0f} VND."
        )

    if "chi tiêu" in text or "tổng chi" in text:
        return (
            f"Tổng chi tháng {month}/{current_year} của bạn là "
            f"{monthly['total_expense']:,.0f} VND."
        )

    if "số dư" in text or "còn lại" in text:
        return (
            f"Số dư tháng {month}/{current_year} của bạn là "
            f"{monthly['balance']:,.0f} VND. "
            f"Tổng thu: {monthly['total_income']:,.0f} VND, "
            f"tổng chi: {monthly['total_expense']:,.0f} VND."
        )

    return None


def get_saving_advice(user_question=None):
    finance_summary = get_finance_summary_text()

    if user_question is None or user_question.strip() == "":
        user_question = "Hãy phân tích tình hình thu chi và đề xuất cách tiết kiệm cho tôi."

    fast_answer = answer_fast_finance_question(user_question)

    if fast_answer:
        return fast_answer

    prompt = f"""
Dữ liệu tài chính:
{finance_summary}

Câu hỏi:
{user_question}

Hãy đưa ra đề xuất tiết kiệm bằng tiếng Việt, tối đa 3 câu.
Không bịa số liệu.
"""

    ai_results = run_parallel_ai(
        {
            "Llama AI": ask_llama,
            "Mistral AI": ask_mistral
        },
        prompt
    )

    return combine_answers_to_one(ai_results, finance_summary)


def get_extra_finance_analysis(user_question=None):
    finance_summary = get_finance_summary_text()

    if user_question is None or user_question.strip() == "":
        user_question = "Hãy phát hiện điểm bất thường trong chi tiêu của tôi."

    prompt = f"""
Dữ liệu tài chính:
{finance_summary}

Yêu cầu:
{user_question}

Hãy phát hiện điểm bất thường hoặc rủi ro tài chính.
Trả lời tiếng Việt, tối đa 3 câu.
Không bịa số liệu.
"""

    ai_results = run_parallel_ai(
        {
            "Gemma AI": ask_gemma,
            "DeepSeek AI": ask_deepseek
        },
        prompt
    )

    return combine_answers_to_one(ai_results, finance_summary)