# SXbot

Chatbot web con modelos open source via Hugging Face.

## Usar solo con GitHub (sin instalar nada en tu PC)

1. Crea el repositorio en GitHub.
2. Sube estos archivos desde la web.
3. Agrega tu token en **Settings > Secrets and variables > Codespaces**.
4. Abre **Code > Codespaces > Create codespace**.
5. En la terminal del codespace:

```bash
cp .env.example .env
python -m app.main
```

Abre el puerto 8000 cuando GitHub te lo sugiera.
