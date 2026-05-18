FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY src/ ./src
COPY alembic/ ./alembic
COPY alembic.ini ./alembic.ini

EXPOSE 8000

CMD ["sh", "-c", "python -m alembic upgrade head && python -m uvicorn src.main:app --host 0.0.0.0 --port 8000"]