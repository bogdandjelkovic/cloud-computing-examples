FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]