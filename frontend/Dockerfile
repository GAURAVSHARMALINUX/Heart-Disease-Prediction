FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations and collect static files
RUN python manage.py migrate

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "heart_disease_app.wsgi:application"]
