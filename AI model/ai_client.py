import requests


def ask_ollama(prompt: str, model: str = "llama3.1") -> str | None:
    """
    Gọi Ollama local để lấy phản hồi AI.
    Nếu lỗi sẽ in lỗi thật ra terminal.
    """
    try:
        url = "http://localhost:11434/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(url, json=payload, timeout=90)
        response.raise_for_status()

        data = response.json()
        answer = data.get("response", "").strip()

        if not answer:
            print("AI trả về rỗng:", data)
            return None

        return answer

    except requests.exceptions.ConnectionError:
        print("LỖI: Không kết nối được Ollama. Hãy kiểm tra Ollama đã chạy chưa.")
        return None

    except requests.exceptions.Timeout:
        print("LỖI: Ollama phản hồi quá lâu, bị timeout.")
        return None

    except Exception as e:
        print("LỖI KHI GỌI OLLAMA:", e)
        return None