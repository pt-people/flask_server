FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_ENV=prod
ENV APP_PORT=5000

CMD ["python", "app.py"]

