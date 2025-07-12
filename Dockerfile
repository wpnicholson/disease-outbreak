FROM python:3.11-slim

LABEL maintainer="Dr. William Nicholson <williampnicholson@gmail.com>"
LABEL version="0.1.0"
LABEL description="Disease Outbreak Reporting System"

ENV PYTHONUNBUFFERED=1

# Install build dependencies required to compile `psycopg2`.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
