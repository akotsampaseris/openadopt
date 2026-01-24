# Stage 1: Build frontend
FROM node:22-alpine AS web-builder

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /web

# Copy package files
COPY web/package.json web/pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy frontend source
COPY web/ ./

# Build frontend
RUN pnpm run build


# Stage 2: Python backend
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy backend dependency files
COPY api/pyproject.toml api/uv.lock* ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Copy backend code
COPY api/ ./

# Copy built frontend from stage 1
COPY --from=web-builder /web/dist ./static

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]