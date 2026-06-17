# parallel_ai.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from ai_providers import ask_llama


def run_parallel_ai(ai_functions: dict, prompt: str, timeout: int = 180) -> dict:
    """
    Chạy nhiều AI song song.
    """
    results = {}

    if not ai_functions:
        return results

    with ThreadPoolExecutor(max_workers=len(ai_functions)) as executor:
        future_to_name = {
            executor.submit(func, prompt): name
            for name, func in ai_functions.items()
        }

        for future in as_completed(future_to_name):
            name = future_to_name[future]

            try:
                answer = future.result(timeout=timeout)

                if answer and str(answer).strip() != "":
                    results[name] = str(answer).strip()
                else:
                    results[name] = f"[{name} lỗi] Không có phản hồi."

            except Exception as e:
                results[name] = f"[{name} lỗi] {e}"

    return results


def combine_answers_to_one(results: dict, finance_summary: str) -> str:
    """
    Tổng hợp nhiều phản hồi AI thành một câu trả lời cuối.
    Dùng Llama làm model tổng hợp.
    """
    valid_answers = []
    error_answers = []

    for name, answer in results.items():
        if not answer:
            continue

        answer = str(answer).strip()

        if answer.startswith("["):
            error_answers.append(answer)
        else:
            valid_answers.append(f"{name}: {answer}")

    if not valid_answers:
        error_text = "\n".join(f"- {err}" for err in error_answers)

        return f"""
Hiện tại hệ thống chưa nhận được phản hồi phù hợp từ AI.

Dữ liệu tài chính hiện có:
{finance_summary}

Lỗi AI ghi nhận:
{error_text if error_text else "- Không có thông tin lỗi."}
""".strip()

    if len(valid_answers) == 1:
        return valid_answers[0].split(":", 1)[1].strip()

    ai_raw_text = "\n\n".join(valid_answers)

    final_prompt = f"""
Bạn là AI tổng hợp câu trả lời cuối cùng cho một hệ thống quản lý tài chính cá nhân.

Dữ liệu tài chính thật:
{finance_summary}

Các phản hồi thô từ nhiều AI:
{ai_raw_text}

Nhiệm vụ:
Hãy tổng hợp thành MỘT câu trả lời cuối cùng cho người dùng.

Yêu cầu bắt buộc:
1. Trả lời bằng tiếng Việt tự nhiên, dễ hiểu.
2. Không ghi "AI này nói", "AI kia nói", "Nhận xét tổng hợp", "Bổ sung".
3. Không bịa số liệu.
4. Không lặp lại quá nhiều số liệu.
5. Giữ lại ý đúng và hữu ích nhất từ các phản hồi.
6. Nếu các phản hồi mâu thuẫn, hãy ưu tiên ý dựa sát dữ liệu tài chính thật.
7. Câu trả lời phải đủ sâu, có phân tích và có gợi ý hành động.
8. Nếu câu hỏi đơn giản thì trả lời ngắn.
9. Nếu câu hỏi cần lập kế hoạch thì trả lời chi tiết hơn.
10. Không trả lời chung chung.

Cấu trúc nên dùng:
- Kết luận chính
- Phân tích dựa trên số liệu
- Gợi ý hành động
- Hướng khác có thể cân nhắc, nếu phù hợp

Hãy viết như một trợ lý tài chính đang tư vấn cho sinh viên.
"""

    final_answer = ask_llama(final_prompt)

    if final_answer and not str(final_answer).startswith("["):
        return final_answer.strip()

    return valid_answers[0].split(":", 1)[1].strip()