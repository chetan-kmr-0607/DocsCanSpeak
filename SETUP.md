# Setup Guide

## Prerequisites

- Python 3.9 or higher
- [Ollama](https://ollama.com) installed (runs the local LLM)

## 1. Clone the repo

```bash
git clone https://github.com/chetan-kmr-0607/DocsCanSpeak.git
cd DocsCanSpeak
```

## 2. Create a virtual environment

A virtual environment keeps this project's Python packages isolated from your system Python and other projects.

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

Your terminal prompt should now start with `(venv)`. You'll need to re-run the `source` line every time you open a new terminal for this project.

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Pull the local LLM

```bash
ollama pull llama3.2
```

One-time download, ~2GB. Make sure the Ollama app is running in the background (check your Mac's menu bar) before continuing.

## 5. Launch the app

```bash
python3 -m streamlit run app.py
```

(Using `python3 -m streamlit` instead of a bare `streamlit run` avoids conflicts if you have Anaconda or another Python distribution installed alongside your venv.)

This opens a browser tab at `localhost:8501`. Drag and drop a PDF, then ask questions about it.

## Troubleshooting

**`ModuleNotFoundError` for a package you know you installed**
Check your virtual environment is active (`(venv)` should be visible in your prompt) and confirm you're using the right Python:
```bash
which python3
```
It should point to a path inside your project's `venv/` folder, not a system or Anaconda Python.

**`streamlit: command not found` or it launches from the wrong Python**
Run it explicitly through your venv's Python instead:
```bash
python3 -m streamlit run app.py
```

**Ollama connection errors**
Make sure the Ollama app is actually running (not just installed) — it needs to be active in the background for `ollama.chat()` calls to work.

**First question after launching feels slow**
Normal — the local model loads into memory on first use. Subsequent questions are faster.
