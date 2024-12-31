
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY nfl_api.py .
COPY nfl_model.joblib .
COPY nfl_scaler.joblib .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "nfl_api:app", "--host", "0.0.0.0", "--port", "8000"]
