# parallel_ai.py

from concurrent.futures import ThreadPoolExecutor, as_completed


def run_parallel_ai(ai_functions: dict, prompt: str, timeout: int = 90) -> dict:
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
                    results[name] = answer.strip()

            except Exception as e:
                results[name] = f"[{name} lỗi] {e}"

    return results


def combine_answers_to_one(results: dict, finance_summary: str) -> str:
    valid_answers = []

    for _, answer in results.items():
        if not answer:
            continue

        if str(answer).startswith("["):
            continue

        valid_answers.append(answer.strip())

    if not valid_answers:
        return f"""
Dựa trên dữ liệu hiện tại:

{finance_summary}

Hệ thống chưa nhận được phản hồi phù hợp từ AI. Tuy nhiên, bạn nên theo dõi nhóm chi tiêu lớn nhất và hạn chế các khoản không cần thiết.
""".strip()

    if len(valid_answers) == 1:
        return valid_answers[0]

    return f"""
Dựa trên dữ liệu tài chính hiện tại:

{finance_summary}

Nhận xét tổng hợp:
{valid_answers[0]}

Bổ sung:
{valid_answers[1]}
""".strip()