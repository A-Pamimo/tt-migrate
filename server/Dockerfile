FROM python:3.11-slim

WORKDIR /workspace/server

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads exports

ENV PYTHONPATH=/workspace

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "/workspace"]
