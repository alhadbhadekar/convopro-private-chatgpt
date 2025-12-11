# ConvoPro – Private ChatGPT Clone

ConvoPro is a lightweight, secure, and fully customizable ChatGPT-style application powered by **Ollama**, **Streamlit**, and **MongoDB Atlas**. It allows you to run private AI chat sessions using local LLMs while storing conversation history securely in a cloud database.

This project is ideal for:

* Personal AI assistants
* Private self-hosted ChatGPT alternatives
* Corporate/internal knowledge assistants
* Developers experimenting with LLM UI + backend integrations

---

# ✨ Features

* 🔒 **100% private** – your data stays with you.
* 🤖 **Local LLMs via Ollama** (supports CPU or GPU).
* 💬 **Clean ChatGPT-style UI** (Streamlit Chat API).
* 🧠 **Automatic conversation titles** based on first message.
* 🗂️ **Chat history stored in MongoDB Atlas**.
* 🚀 **Fast and lightweight** – runs even on small EC2 instances.
* 🖥️ **Supports multiple models** (choose any Ollama model).
* 🌐 **One-click deployment to AWS EC2**.

---

# 🏗️ Architecture

```
Streamlit UI → Python App → Ollama API → LLM Response
                    ↓
              MongoDB Atlas
```

---

# 📦 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **LLM Runtime:** Ollama
* **Database:** MongoDB Atlas
* **Deployment:** AWS EC2 (Ubuntu)
* **Containerization:** Docker

---

# ⚙️ Requirements

* Python 3.10+ or 3.12
* MongoDB Atlas connection string
* Ollama installed locally OR on EC2
* Supported model pulled (e.g., `llama3.1:1b`)

---

# 🔧 Environment Variables (`.env`)

```
MONGO_DB_URL="mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME="chat_data"

OLLAMA_URL="http://localhost:11434"
OLLAMA_MODELS="llama3.1:1b"
```

---

# 🧑‍💻 Local Development Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/<yourname>/convopro-private-chatgpt.git
cd convopro-private-chatgpt
```

### 2️⃣ Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Configure `.env`

Fill in your MongoDB Atlas credentials and Ollama settings.

### 5️⃣ Run the app

```
streamlit run main.py
```

App runs at:
👉 [http://localhost:8501/](http://localhost:8501/)

---

# 🚀 Deployment on AWS EC2 (t3.micro, Free Tier)

This section explains how to deploy ConvoPro on an EC2 instance.

## ✅ **Instance Requirements**

* Ubuntu 24.04
* t3.micro (FREE)
* Open Ports: **8501**, **11434**, **22**

## 📜 **One‑Command Setup Script**

Paste this entire block into the EC2 terminal:

```
#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

sudo apt install -y python3 python3-pip python3.12-venv git
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker

docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker exec -it ollama ollama pull llama3.1:1b

git clone https://github.com/alhadbhadekar/convopro-private-chatgpt.git convopro
cd convopro

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cat <<EOF > .env
MONGO_DB_URL="mongodb+srv://alhad:Ab080691@cluster0.ov08bfm.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME="chat_data"

OLLAMA_URL="http://localhost:11434"
OLLAMA_MODELS="llama3.1:1b"
EOF

nohup streamlit run main.py --server.port=8501 --server.address=0.0.0.0 > app.log 2>&1 &

echo "ConvoPro is live at: http://$(curl -s ifconfig.me):8501"
```

## 🔥 After Deployment

Visit your live app:
👉 `http://<EC2_PUBLIC_IP>:8501`

Check logs:

```
tail -f app.log
```

Restart app:

```
pkill -f streamlit
nohup streamlit run main.py --server.port=8501 --server.address=0.0.0.0 &
```

---

# 🗄️ MongoDB Schema

### Conversation Document

```
{
  _id: "uuid",
  title: "Conversation Title",
  messages: [
    { role: "user", content: "Hello", timestamp: <date> },
    { role: "assistant", content: "Hi there!", timestamp: <date> }
  ],
  last_interacted: <ISODate>
}
```

---

# 🧪 Testing

```
pytest
```

(If tests exist — optional.)

---

# 🛠️ Troubleshooting

### ❌ *Model not found*

Pull the model manually:

```
docker exec -it ollama ollama pull llama3.1:1b
```

### ❌ *Streamlit not running*

```
ps aux | grep streamlit
```

### ❌ *MongoDB connection error*

Whitelist your EC2 IP in MongoDB Atlas.

---

# 📜 License

MIT — free to modify and use.

---

# ❤️ Support

If you'd like enhancements, optimizations, or custom features, feel free to reach out.

ConvoPro is built to be **simple, private, and powerful** — enjoy your personal ChatGPT! 🚀
