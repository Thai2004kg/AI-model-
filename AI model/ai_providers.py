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
    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 120
            }
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=90
        )

        response.raise_for_status()
        data = response.json()

        return data.get("response", "").strip()

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