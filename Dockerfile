FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure data is downloaded and models are trained during build (or expect them to be provided)
# For a production container, we might train beforehand and just copy the models/ folder.
# Here we will expect models to be present or run the train script.
RUN python data/download_data.py && \
    python -m src.train

EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
