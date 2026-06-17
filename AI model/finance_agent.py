# finance_agent.py

from database import get_finance_summary_text

from ai_providers import (
    ask_llama,
    ask_mistral,
    ask_qwen,
    ask_gemma,
    ask_phi,
    ask_deepseek
)

from parallel_ai import run_parallel_ai, combine_answers_to_one
from prompt_builder import build_finance_prompt


def ask_finance_agent(user_question: str):
    """
    AI Agent hỏi đáp tài chính.
    Không dùng trả lời nhanh bằng Python.
    Mọi câu hỏi đều đưa cho AI xử lý.
    SQLite chỉ cung cấp dữ liệu thật.
    """

    if user_question is None or user_question.strip() == "":
        return "Bạn hãy nhập câu hỏi trước."

    finance_summary = get_finance_summary_text()

    prompt = build_finance_prompt(
        user_question=user_question,
        finance_summary=finance_summary,
        task_type="general"
    )

    ai_results = run_parallel_ai(
        {
            "Llama AI": ask_llama,
            "Mistral AI": ask_mistral,
            "Qwen AI": ask_qwen,
            "Gemma AI": ask_gemma,
            "Phi AI": ask_phi,
            "DeepSeek AI": ask_deepseek
        },
        prompt,
        timeout=180
    )

    return combine_answers_to_one(ai_results, finance_summary)