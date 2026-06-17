# saving_advisor.py

from database import get_finance_summary_text

from ai_providers import (
    ask_llama,
    ask_mistral,
    ask_gemma,
    ask_deepseek
)

from parallel_ai import run_parallel_ai, combine_answers_to_one
from prompt_builder import build_finance_prompt


def get_saving_advice(user_question=None):
    """
    Đề xuất tiết kiệm bằng AI only.
    """

    finance_summary = get_finance_summary_text()

    if user_question is None or user_question.strip() == "":
        user_question = "Hãy phân tích tình hình thu chi và đề xuất cách tiết kiệm cho tôi."

    prompt = build_finance_prompt(
        user_question=user_question,
        finance_summary=finance_summary,
        task_type="saving"
    )

    ai_results = run_parallel_ai(
        {
            "Llama AI": ask_llama,
            "Mistral AI": ask_mistral
        },
        prompt,
        timeout=180
    )

    return combine_answers_to_one(ai_results, finance_summary)


def get_extra_finance_analysis(user_question=None):
    """
    Phân tích bất thường bằng AI only.
    """

    finance_summary = get_finance_summary_text()

    if user_question is None or user_question.strip() == "":
        user_question = "Hãy phát hiện điểm bất thường trong chi tiêu của tôi."

    prompt = build_finance_prompt(
        user_question=user_question,
        finance_summary=finance_summary,
        task_type="anomaly"
    )

    ai_results = run_parallel_ai(
        {
            "Gemma AI": ask_gemma,
            "DeepSeek AI": ask_deepseek
        },
        prompt,
        timeout=180
    )

    return combine_answers_to_one(ai_results, finance_summary)