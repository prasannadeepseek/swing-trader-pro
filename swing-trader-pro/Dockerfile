# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install -r requirements.txt && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y

CMD ["python", "main.py"]