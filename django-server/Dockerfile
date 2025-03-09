FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -la /app

EXPOSE 8000

CMD ["gunicorn", "--bind", "127.0.0.1:8000", "--no-reload", "core.wsgi:application"]
