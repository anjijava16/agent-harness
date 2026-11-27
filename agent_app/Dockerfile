FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY ui ./ui
COPY usecases ./usecases
EXPOSE 8000
# One worker: paused runs live in this process. See README, "Going to production".
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
