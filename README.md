# 📝 Text Summarizer

A [Gradio](https://www.gradio.app/) web app that produces a concise summary of the pasted text with a single OpenAI Chat Completions API call (default model: `gpt-4o-mini`).

## Features

- The summary is written in the same language as the input text.
- Three length options: "Very short (1-2 sentences)", "Short (3-5 sentences)", "Detailed (one paragraph)".
- Clean output: only the summary, with no preambles like "Sure, here is the summary...". This is achieved with a strict system prompt, `temperature=0.2` and `.strip()`.
- Clear error messages: empty key or text, text too long, invalid key, rate limit, network problems.
- The API key is entered in the UI (a `password` field) and is never stored in code, files or logs.

## Configuration

All settings live in `Settings` (`config.py`) and are injected into `Summarizer` and the UI. Defaults can be overridden with environment variables:

| Variable | Default |
|---|---|
| `SUMMARIZER_MODEL` | `gpt-4o-mini` |
| `SUMMARIZER_TEMPERATURE` | `0.2` |
| `SUMMARIZER_MAX_INPUT_CHARS` | `30000` |
| `SUMMARIZER_REQUEST_TIMEOUT` | `60` |

## Running locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open the URL printed by Gradio (usually http://127.0.0.1:7860), then enter your OpenAI API key and a text.

## Deploying to Render

The repository includes a [Render Blueprint](https://render.com/docs/blueprint-spec) (`render.yaml`) that runs the app as a free web service.

1. Push the repository to GitHub.
2. In the [Render dashboard](https://dashboard.render.com), choose **New → Blueprint** and select the repository.
3. Render installs `requirements.txt` and starts `python app.py`. Gradio binds to `0.0.0.0:10000` through the `GRADIO_SERVER_NAME` and `GRADIO_SERVER_PORT` variables set in `render.yaml`.

No secrets are needed: every user enters their own key in the UI. Free services sleep when idle, so the first request after a pause can take up to a minute.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Gradio UI and entry point |
| `summarizer.py` | `Summarizer`: prompt, validation and the OpenAI call (UI-independent) |
| `config.py` | `Settings`: model, temperature, limits, length presets |
| `requirements.txt` | Dependencies: `gradio`, `openai` |
| `render.yaml` | Render deployment blueprint |
| `SUBMISSION.md` | Short project description for submission |
