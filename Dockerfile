# Stage 1: Build React frontend
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./

RUN npm install -g npm@12.2.2
RUN npm ci --no-audit --no-fund || (cat /root/.npm/_logs/*debug-0.log; exit 1)

COPY frontend/ ./

RUN npm run build

# Stage 2: Run FastAPI backend
FROM python:3.11-slim AS backend

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY api.py ./
COPY shadowsaas/ ./shadowsaas/

COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
