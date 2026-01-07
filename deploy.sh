#!/usr/bin/env bash
set -euo pipefail

# One-click helper to bring up core infra (MySQL + MinIO) and prep backend/frontend.
# Prereqs: docker, docker-compose (v2), python3, node/npm (or pnpm).

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${ROOT_DIR}/.deploy/docker-compose.yml"

mkdir -p "${ROOT_DIR}/.deploy"

cat > "${COMPOSE_FILE}" <<'EOF'
version: "3.8"
services:
  mysql:
    image: mysql:8
    container_name: ztb_mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: ztb
    ports:
      - "3306:3306"
    volumes:
      - ztb_mysql_data:/var/lib/mysql

  minio:
    image: quay.io/minio/minio
    container_name: ztb_minio
    restart: unless-stopped
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - ztb_minio_data:/data

  # Optional: Ollama (you still need to pull models, e.g., `ollama pull qwen2:7b`)
  ollama:
    image: ollama/ollama:latest
    container_name: ztb_ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ztb_ollama_data:/root/.ollama

  # Optional: AnythingLLM (configure UI at http://localhost:3001)
  anythingllm:
    image: mintplexlabs/anythingllm:latest
    container_name: ztb_anythingllm
    restart: unless-stopped
    environment:
      STORAGE_DIR: /app/storage
    ports:
      - "3001:3001"
    volumes:
      - ztb_anything_storage:/app/storage

volumes:
  ztb_mysql_data:
  ztb_minio_data:
  ztb_ollama_data:
  ztb_anything_storage:
EOF

echo "Starting infra containers (MySQL, MinIO, Ollama, AnythingLLM)..."
docker compose -f "${COMPOSE_FILE}" up -d

echo "Importing schema.sql into MySQL..."
docker exec -i ztb_mysql sh -c "mysql -uroot -ppassword ztb" < "${ROOT_DIR}/backend_service/schema.sql" || true

echo "Backend env template (.env) is in backend_service/.env.example"
echo "Frontend env template (.env) is in ui_service/.env.example"

echo "To run backend locally:"
echo "  cd backend_service"
echo "  python -m venv .venv && source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  cp .env.example .env  # adjust endpoints if not default"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000"

echo "To run frontend locally:"
echo "  cd ui_service"
echo "  npm install"
echo "  cp .env.example .env"
echo "  npm run dev -- --host --port 3000"

echo "Services:"
echo "  MySQL:      localhost:3306 (user: root / password)"
echo "  MinIO:      localhost:9000 (console :9001, user: minioadmin / minioadmin)"
echo "  Ollama:     localhost:11434 (pull models manually)"
echo "  AnythingLLM: http://localhost:3001 (configure API key via UI, then set backend env)"
