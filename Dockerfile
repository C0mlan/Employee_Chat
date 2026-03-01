FROM python:3.11-slim

# Prevent Python from buffering logs (important for Celery)
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /code/


RUN chmod -R 777 /code