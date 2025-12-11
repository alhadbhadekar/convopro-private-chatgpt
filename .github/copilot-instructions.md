# Copilot / AI Agent Instructions for convoPro (private)

This file gives focused, actionable guidance for AI coding agents working in this repository.

Summary
- **Purpose**: Small Streamlit + LLM integration project (see `requirements.txt`).
- **Key libraries**: `streamlit`, `ollama`, `llama-index`, `pymongo`, `pydantic`, `python-dotenv`.

What to look for first
- Open `requirements.txt` to see runtime dependencies and the LLM stack used.
- `README.md` is currently empty — use it as the canonical place to add high-level run/setup steps.

Architecture / Big picture (discoverable patterns)
- UI: likely a Streamlit app (run via `streamlit run <app_file>.py`). Search for files that import `streamlit`.
- LLM layer: `ollama` + `llama-index` are installed — expect code that constructs an index and calls an Ollama LLM backend. Look for imports like `from llama_index import ...` or `import ollama`.
- Persistence: `pymongo` is present — DB-backed document storage or user/session persistence may exist; look for `pymongo.MongoClient` usage.
- Validation/config: `pydantic` and `pydantic-settings` indicate model-based config/validation; search for `BaseModel`/`Settings` subclasses.

Developer workflows and explicit commands
- Create virtualenv and install deps:
  - `python -m venv .venv`
  - `source .venv/bin/activate` (macOS zsh)
  - `pip install -r requirements.txt`
- Run the app (common pattern for Streamlit):
  - `streamlit run app.py` (replace `app.py` with the top-level Streamlit file — search for `streamlit` imports to find the exact file)
- Environment: project uses `python-dotenv` — expect a `.env` file for keys (Ollama host/model names, Mongo URI). Do not commit secrets.

Project-specific conventions and tips for editing
- If you add runtime config, prefer `pydantic` settings models (project already uses `pydantic-settings`).
- When changing LLM calls, keep model and generation parameters configurable via environment or a `Settings` class.
- Use Mongo connection strings from environment and protect them with `pydantic` validators.

Integration points to check before making changes
- Ollama: confirm local Ollama daemon and models are used; code may call `ollama.Client` or shell out — search for `ollama` references.
- Llama-Index: inspect how indexes are built/serialized. Large indices should not be rebuilt on every run; prefer persisted indices (file or DB).
- Streamlit state: if the app uses `st.session_state`, preserve keys when refactoring and avoid reinitializing state on every rerun.

What to avoid / assumptions
- Do not hardcode API keys, hostnames, or DB URIs — use `.env` + `pydantic` settings.
- Avoid rebuilding heavy indices in UI request paths; move expensive work to startup or background jobs.

Examples from this repo
- `requirements.txt`: shows `streamlit`, `ollama`, `llama-index`, `pymongo`, `pydantic`, `python-dotenv` — use these as anchors when searching for related code.
- `README.md` is empty: add run instructions and environment variable examples here if you edit the repo.

If you cannot find expected files
- If `streamlit` imports are missing, search for files referencing `llama_index` or `ollama` — the app may be split into modules.
- If no tests or CI configs are present, add focused unit tests for parsing/validation code and a simple integration test that mounts the LLM client with a mock/stub.

When you finish a change
- Update `README.md` with run steps and environment variable names you touched.
- Leave a concise PR description explaining runtime effects (e.g., "persist index to `data/index.bin`" or "add `Settings` for Ollama host").

Questions for the maintainer (leave in PR description)
- Which file is the main Streamlit entrypoint? (used for run commands in README)
- Where should persisted indices or cached artifacts be stored (repo `data/` or external storage)?

If anything in this file is unclear, ask for the main entrypoint filename and any expected env var names — I will iterate.
