convopro — Streamlit + LLM quick-start

Quick setup

1. Create a Python virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.sample` to `.env` and fill values for your environment (Ollama host/model, Mongo URI):

```bash
cp .env.sample .env
# edit .env to add secrets
```

Running the app

- This repository currently contains only `requirements.txt`. Search for the Streamlit entrypoint with:

```bash
grep -R "import streamlit" -n . || true
```

- Common run command (replace `app.py` when you identify the entrypoint):

```bash
streamlit run app.py
```

Next steps (recommended)

- Tell me which file is the main Streamlit entrypoint and preferred index storage path. I can then:
	- scaffold a minimal `app.py` that wires `ollama` + `llama-index` + `pymongo` using `pydantic` settings.
	- add index persistence (e.g., `data/index.bin`) and runtime `st.session_state` patterns.

Contact

If anything above is unclear, reply with your preferred app filename and any environment variables you plan to provide.

