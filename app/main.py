from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.config import APP_HOST, APP_PORT, AVAILABLE_MODELS, HF_MODEL
from app.hf_client import ChatbotError, chat

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="SXbot", description="Chatbot con modelos open source via Hugging Face")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[dict[str, str]] = Field(default_factory=list)
    model: str | None = None


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    html_path = BASE_DIR / "templates" / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/api/models")
def list_models() -> dict:
    return {"default": HF_MODEL, "models": AVAILABLE_MODELS}


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    selected_model = payload.model or HF_MODEL
    messages = [
        {
            "role": "system",
            "content": "Eres SXbot, un asistente util, claro y amigable. Responde en espanol.",
        },
        *payload.history,
        {"role": "user", "content": payload.message.strip()},
    ]

    try:
        reply = chat(messages, model=selected_model)
    except ChatbotError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ChatResponse(reply=reply, model=selected_model)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=APP_HOST, port=APP_PORT, reload=True)
