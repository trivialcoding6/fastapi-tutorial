# syntax=docker/dockerfile:1
FROM python:3.11-slim

# 시스템 패키지 업데이트 및 필요한 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Poetry 설치 및 설정
ENV POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HTTP_TIMEOUT=120

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# 의존성 파일 복사 및 설치
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-root

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV PYTHONPATH=/app

EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]