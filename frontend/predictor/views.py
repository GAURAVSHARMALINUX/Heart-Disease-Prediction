from django.shortcuts import render
from django.conf import settings
import requests
import json

def index(request):
    result = None
    error = None
    if request.method == "POST":
        try:
            payload = {
                "age": float(request.POST.get("age")),
                "sex": int(request.POST.get("sex")),
                "cp": int(request.POST.get("cp")),
                "trestbps": float(request.POST.get("trestbps")),
                "chol": float(request.POST.get("chol")),
                "fbs": int(request.POST.get("fbs")),
                "restecg": int(request.POST.get("restecg")),
                "thalach": float(request.POST.get("thalach")),
                "exang": int(request.POST.get("exang")),
                "oldpeak": float(request.POST.get("oldpeak")),
                "slope": int(request.POST.get("slope")),
                "ca": float(request.POST.get("ca")),
                "thal": int(request.POST.get("thal"))
            }
            
            response = requests.post(settings.BACKEND_API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                result = {
                    "prediction": data.get("prediction"),
                    "confidence": round(data.get("confidence", 0) * 100, 2)
                }
            else:
                error = f"Backend API Error: {response.status_code} - {response.text}"
        except Exception as e:
            error = f"Error processing request: {str(e)}"
            
    return render(request, "predictor/index.html", {"result": result, "error": error})
