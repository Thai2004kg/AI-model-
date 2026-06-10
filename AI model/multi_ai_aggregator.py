# multi_ai_aggregator.py

from ai_providers import (
    ask_llama,
    ask_mistral,
    ask_qwen,
    ask_gemma,
    ask_phi,
    ask_deepseek,
)


def collect_ai_answers(prompt: str, finance_summary: str = "") -> dict:
    results = {}

    providers = {
        "Llama AI": ask_llama(prompt),
        "Mistral AI": ask_mistral(prompt),
        "Qwen AI": ask_qwen(prompt),
        "Gemma AI": ask_gemma(prompt),
        "Phi AI": ask_phi(prompt),
        "DeepSeek AI": ask_deepseek(prompt),
    }

    for name, answer in providers.items():
        if answer is not None and str(answer).strip() != "":
            results[name] = answer

    return results


def aggregate_answers(user_question: str, finance_summary: str, ai_results: dict) -> str:
    ai_text = ""

    for ai_name, answer in ai_results.items():
        ai_text += f"\n--- {ai_name} ---\n{answer}\n"

    final_prompt = f"""
Bạn là AI tổng hợp kết quả phân tích tài chính cá nhân.

Câu hỏi của người dùng:
{user_question}

Dữ liệu tài chính thật từ SQLite:
{finance_summary}

Dưới đây là kết quả phân tích từ 6 mô hình AI khác nhau:
{ai_text}

Nhiệm vụ:
- Tổng hợp thành MỘT câu trả lời duy nhất.
- Không liệt kê từng AI.
- Không nói "theo AI này" hoặc "theo AI kia".
- Không bịa số liệu.
- Nếu dữ liệu chưa đủ thì nói rõ.
- Trả lời bằng tiếng Việt.
- Câu trả lời ngắn gọn, dễ hiểu, có lời khuyên cụ thể.
"""

    # Dùng Llama làm AI tổng hợp cuối cùng
    final_answer = ask_llama(final_prompt)

    if final_answer and not final_answer.startswith("["):
        return final_answer

    return manual_aggregate_answer(finance_summary)


def manual_aggregate_answer(finance_summary: str) -> str:
    return f"""
Dựa trên dữ liệu hiện tại, hệ thống ghi nhận tình hình thu chi như sau:

{finance_summary}

Gợi ý tiết kiệm: bạn nên theo dõi nhóm chi tiêu lớn nhất và đặt giới hạn cho nhóm đó. Nếu tổng chi gần bằng tổng thu, nên giảm các khoản không thiết yếu như ăn uống bên ngoài, mua sắm hoặc giải trí.
""".strip()