FROM python:3.12.4-slim-bookworm
RUN apt-get update && \
    apt-get install -y cargo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8002
CMD ["uvicorn", "main:app", "--port", "8002"]
