#!/bin/bash

echo "=================================="
echo "   EC2 SETUP FOR CONVOPRO"
echo "=================================="

echo "=== Updating system ==="
sudo apt update -y
sudo apt upgrade -y

echo "=== Installing Python, Git, pip, venv ==="
sudo apt install -y python3 python3-pip python3.12-venv git

echo "=== Installing Docker ==="
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker

echo "=== Running Ollama (CPU mode, no GPU) ==="
sudo docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama

echo "=== Pulling SMALL RAM-FRIENDLY MODEL FOR t3.micro ==="
sudo docker exec -it ollama ollama pull llama3.1:1b

echo "=== Cloning your GitHub repo ==="
git clone https://github.com/alhadbhadekar/convopro-private-chatgpt.git convopro
cd convopro

echo "=== Creating Python venv ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Installing requirements ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Creating .env file ==="
cat <<EOF > .env
MONGO_DB_URL="mongodb+srv://alhad:<NEW_PASSWORD>@cluster0.ov08bfm.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME="chat_data"

OLLAMA_URL="http://localhost:11434"
OLLAMA_MODELS="llama3.1:1b"
EOF

echo "=== Running Streamlit app in background ==="
nohup streamlit run main.py --server.port=8501 --server.address=0.0.0.0 > app.log 2>&1 &

echo "=== DONE! ==="
echo "Your ConvoPro app is live at:"
echo "👉 http://$(curl -s ifconfig.me):8501"
echo "=================================="
