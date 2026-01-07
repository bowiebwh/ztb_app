# ztb_app 部署与功能指南

本项目提供招标文件解析、占位符式标书编辑、素材绑定、自动生成与导出 Word 的全链路能力。后端基于 FastAPI，前端基于 Vue 3，依赖 MySQL、MinIO、Ollama（本地大模型）、AnythingLLM（知识库）。

## 功能概览
- 招标文件上传与解析：上传后通过 `/api/pipeline/ingest/{projectId}` 建立索引、抽取结构。
- 分析与提纲：`/api/analysis/{projectId}` 调用本地 LLM 与知识库生成概要、关键日期、章节结构。
- 素材库与占位符绑定：`/api/materials/upload` 上传素材；编辑页将素材绑定占位符（如 image_placeholder/table_placeholder），触发 `/api/materials/bind` 保存结构。
- 内容生成：`/api/generation/{projectId}` 或 `/api/chapters/{projectId}` 生成章节，可用 `/latest`、`/history` 查看进度。
- 导出 Word：`/api/export/word` 生成符合投标书样式的 DOCX，返回下载 URL。
- 前端体验：招标文件分析结果展示、章节结构/占位符可视化、素材库管理、拖拽替换占位符、导出入口。

## 从零部署（WSL）
假设代码位于 `/home/<user>/ztb_app`。

### 1) 准备代码
```bash
mkdir -p /home/<user>/ztb_app
# 将仓库放入该目录（git clone 或复制）
```

### 2) 基础环境
- 安装 Docker & docker-compose
- 安装 Python 3
- 安装 Node.js / npm

### 3) 启动依赖（MySQL/MinIO/Ollama/AnythingLLM）
```bash
cd /home/<user>/ztb_app
docker compose -f .deploy/docker-compose.yml up -d
```

导入数据库结构：
```bash
mysql -h127.0.0.1 -uroot -ppassword -P 3307 ztb < backend_service/schema.sql
```

拉取 Ollama 模型（示例：千问/LLama 等）：
```bash
docker exec -it ztb_ollama ollama pull qwen3:14b （推理）
docker exec -it ztb_ollama ollama pull BGE-M3 （Embedding）
```

### 4) 配置 AnythingLLM
- 打开 `http://localhost:3002`
- 配置 ollama服务地址，Workspace（推理模型、embedding模型） 与 API Key（后端 `.env` 需要用到）

### 5) 配置后端环境变量
```bash
cd backend_service
cp .env.example .env
```
`.env` 示例：
```
MYSQL_URL=mysql+pymysql://root:password@localhost:3307/ztb
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=ztb
OLLAMA_BASE=http://localhost:11435
OLLAMA_MODEL=qwen3:14b          # 需已在 Ollama 中 pull
ANYTHINGLLM_BASE=http://localhost:3002
ANYTHINGLLM_API_KEY=你的APIKEY
```

### 6) 启动后端
```bash
cd backend_service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
# 如报错可补充：pip install cryptography
```

### 7) 配置并启动前端
```bash
cd ../ui_service
cp .env.example .env   # 默认 VITE_API_BASE=http://localhost:8000
npm install
npm run dev -- --host --port 3000
# 生产构建：npm run build 后用静态服务器托管 dist
```

## 目录约定
- 代码根：`/home/<user>/ztb_app`
- 后端：`/home/<user>/ztb_app/backend_service`
- 前端：`/home/<user>/ztb_app/ui_service`
- Docker 数据卷：compose 自动创建（MySQL、MinIO、Ollama、AnythingLLM）

## 验证流程（手工回归）
1. 创建项目 → 上传招标文件 `/api/files/upload`  
2. 建立索引：`POST /api/pipeline/ingest/{projectId}`  
3. 分析：`POST /api/analysis/{projectId}`  
4. 上传素材：`POST /api/materials/upload`（前端素材库应显示）  
5. 编辑页：确保 `/api/document/{projectId}/structure` 有占位符，拖拽素材绑定并触发 `/api/materials/bind`  
6. 生成：`POST /api/generation/{projectId}` 或 `/api/chapters/{projectId}`，用 `/latest`、`/history` 查进度  
7. 导出：`POST /api/export/word`，用返回 `url` 下载检查格式  

## 常用端口
- 后端：8000
- 前端：3000
- MySQL：3307（root/password）
- MinIO：9000（控制台 9001，minioadmin/minioadmin）
- Ollama：11435
- AnythingLLM：3002

## 停止与清理
（会清空数据，请确保可重建）
```bash
docker compose -f .deploy/docker-compose.yml down -v
docker rm -f ztb_anythingllm
docker volume rm ztb_anything_storage
docker compose -f .deploy/docker-compose.yml up -d anythingllm
docker inspect ztb_anythingllm | grep -A 5 "Mounts"
```

调试示例：
```bash
curl http://ollama:11434/api/embeddings \
  -d '{"model": "qwen3:14b", "prompt": "Hello, world!"}'
docker compose -f .deploy/docker-compose.yml down
docker compose -f .deploy/docker-compose.yml up -d
```

按以上步骤可在 WSL 一键启动依赖、后端与前端，并完成核心业务流的全链路验证。***
