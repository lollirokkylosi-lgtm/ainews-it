FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crea directory per il DB e i log
RUN mkdir -p logs

CMD ["python", "main.py", "--limit", "10", "--full-text"]
