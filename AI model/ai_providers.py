# ai_providers.py

import requests
from config import (
    OLLAMA_URL,

    USE_LLAMA_AI,
    USE_MISTRAL_AI,
    USE_QWEN_AI,
    USE_GEMMA_AI,
    USE_PHI_AI,
    USE_DEEPSEEK_AI,

    LLAMA_MODEL,
    MISTRAL_MODEL,
    QWEN_MODEL,
    GEMMA_MODEL,
    PHI_MODEL,
    DEEPSEEK_MODEL,
)


def ask_ollama_model(model_name: str, prompt: str) -> str:
    """
    Gọi 1 model Ollama local.
    Nếu lỗi thì trả về chuỗi lỗi để app hiển thị rõ.
    """

    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 500
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=240
        )

        response.raise_for_status()
        data = response.json()

        answer = data.get("response", "").strip()

        if not answer:
            return f"[{model_name} lỗi] AI trả về rỗng."

        return answer

    except requests.exceptions.ConnectionError:
        return (
            f"[{model_name} lỗi] Không kết nối được Ollama. "
            f"Hãy kiểm tra Ollama đã chạy chưa."
        )

    except requests.exceptions.Timeout:
        return (
            f"[{model_name} lỗi] Model phản hồi quá lâu, bị timeout. "
            f"Có thể máy đang quá tải hoặc model quá nặng."
        )

    except Exception as e:
        return f"[{model_name} lỗi] {e}"


def ask_llama(prompt: str) -> str | None:
    if not USE_LLAMA_AI:
        return None

    return ask_ollama_model(LLAMA_MODEL, prompt)


def ask_mistral(prompt: str) -> str | None:
    if not USE_MISTRAL_AI:
        return None

    return ask_ollama_model(MISTRAL_MODEL, prompt)


def ask_qwen(prompt: str) -> str | None:
    if not USE_QWEN_AI:
        return None

    return ask_ollama_model(QWEN_MODEL, prompt)


def ask_gemma(prompt: str) -> str | None:
    if not USE_GEMMA_AI:
        return None

    return ask_ollama_model(GEMMA_MODEL, prompt)


def ask_phi(prompt: str) -> str | None:
    if not USE_PHI_AI:
        return None

    return ask_ollama_model(PHI_MODEL, prompt)


def ask_deepseek(prompt: str) -> str | None:
    if not USE_DEEPSEEK_AI:
        return None

    return ask_ollama_model(DEEPSEEK_MODEL, prompt)