
# Bepu AI - Safe Deploy Package (zip)

This package contains a **safe, minimal** FastAPI server template and deployment files designed to **avoid common Render build failures**.
It intentionally does **not** include heavy binary dependencies (e.g., `rembg` or `onnxruntime`) that frequently cause build failures on low-memory build instances.

## Included files
- main.py            -> Minimal FastAPI app (chat, tts, remove-background proxy)
- requirements.txt   -> Minimal dependencies (no rembg/onnxruntime)
- render.yaml        -> Safe Render service config (do NOT commit secrets here)
- cleanup_commands.sh-> Helper commands to find & redact leaked keys in files (run locally)
- README.md          -> This file

## How to deploy on Render (recommended)
1. Push this repo to your Git provider (GitHub/GitLab).
2. On Render, create a new Web Service and connect your repo.
3. In Render service settings -> Environment, add the sensitive vars (DO NOT commit them):
   - OPENAI_API_KEY = (your OpenAI key)
   - REMOVE_BG_API_KEY = (your remove.bg API key)  # optional, for background removal via remove.bg
4. Ensure the Build Command and Start Command match those in `render.yaml` (or just use the `render.yaml` file).
5. Trigger a Manual Deploy on Render. Check Deploy Logs for errors.

## Background removal options
- **Recommended (no heavy build deps):** Use remove.bg (paid API). Set REMOVE_BG_API_KEY in Render env and the `/remove-background` endpoint will proxy the request.
- **If you prefer local removal:** Install `rembg` and `onnxruntime` in requirements.txt. Warning: this can cause build failures or memory issues on small Render plans. Test locally first with `pip install rembg onnxruntime`.

## Quick local test
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
curl -i http://127.0.0.1:8000/health
```

## If you accidentally leaked OPENAI_API_KEY
Run the `cleanup_commands.sh` (edit the leaked string inside before running). This script shows common `sed`/`git` steps to sanitize repository content locally. For thorough history removal, use BFG Repo-Cleaner (instructions included in script).

---
If you'd like, I can also produce a version that *includes* rembg/onnxruntime (for servers with enough memory) — but that increases the chance of build failure on Render free tier. Ask me and I'll produce that variant.
