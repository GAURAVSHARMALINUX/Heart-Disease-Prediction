from django.shortcuts import render
import requests
import json

# URL of the internal Kubernetes service
# Service Name: heart-disease-service, Port: 80
API_URL = "http://heart-disease-service:80/api/predict"

def index(request):
    prediction = None
    confidence = None
    error = None

    if request.method == 'POST':
        try:
            # Gather data from form
            payload = {
                "age": int(request.POST.get('age')),
                "sex": int(request.POST.get('sex')),
                "cp": int(request.POST.get('cp')),
                "trestbps": int(request.POST.get('trestbps')),
                "chol": int(request.POST.get('chol')),
                "fbs": int(request.POST.get('fbs')),
                "restecg": int(request.POST.get('restecg')),
                "thalach": int(request.POST.get('thalach')),
                "exang": int(request.POST.get('exang')),
                "oldpeak": float(request.POST.get('oldpeak')),
                "slope": int(request.POST.get('slope')),
                "ca": int(request.POST.get('ca')),
                "thal": int(request.POST.get('thal')),
            }

            # Send request to FastAPI backend
            response = requests.post(API_URL, json=payload, timeout=5)
            response.raise_for_status()
            
            # Parse result
            data = response.json()
            pred_val = data.get("prediction")
            confidence_val = data.get("confidence")

            prediction = "Heart Disease Detected" if pred_val == 1 else "No Heart Disease"
            confidence = f"{confidence_val * 100:.2f}%" if confidence_val is not None else "N/A"

        except Exception as e:
            error = f"Error connecting to API: {str(e)}"

    return render(request, 'index.html', {
        'prediction': prediction,
        'confidence': confidence,
        'error': error
    })
