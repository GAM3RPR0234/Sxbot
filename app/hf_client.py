from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError

from app.config import HF_MODEL, HF_TOKEN


class ChatbotError(Exception):
    pass


def _client(model: str | None = None) -> InferenceClient:
    if not HF_TOKEN:
        raise ChatbotError(
            "Falta HF_TOKEN. Crea un archivo .env con tu token de Hugging Face."
        )

    return InferenceClient(model=model or HF_MODEL, token=HF_TOKEN)


def chat(messages: list[dict[str, str]], model: str | None = None) -> str:
    selected_model = model or HF_MODEL

    try:
        response = _client(selected_model).chat_completion(
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
    except HfHubHTTPError as exc:
        detail = str(exc)
        if "401" in detail:
            raise ChatbotError("Token invalido. Revisa HF_TOKEN en tu archivo .env.") from exc
        if "403" in detail:
            raise ChatbotError(
                f"No tienes acceso al modelo '{selected_model}'. "
                "Acepta la licencia en Hugging Face o elige otro modelo."
            ) from exc
        raise ChatbotError(f"Error de Hugging Face: {detail}") from exc
    except Exception as exc:
        raise ChatbotError(f"No se pudo obtener respuesta: {exc}") from exc

    content = response.choices[0].message.content
    if not content:
        raise ChatbotError("El modelo devolvio una respuesta vacia.")

    return content.strip()
