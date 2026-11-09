FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim AS backend
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY api.py ./
COPY shadowsaas/ ./shadowsaas/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
RUN useradd -m appuser
USER appuser
EXPOSE 8000
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
