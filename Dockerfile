FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME ["/data"]

ENV STORAGE_DIR=/data

EXPOSE 3000

CMD ["python", "main.py"]
