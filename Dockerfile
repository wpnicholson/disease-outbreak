FROM python:3.11-slim

LABEL maintainer="Dr. William Nicholson <williampnicholson@gmail.com>"
LABEL version="0.1.0"
LABEL description="Disease Outbreak Reporting System"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
