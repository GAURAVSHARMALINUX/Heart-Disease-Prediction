# API Documentation

The backend service is built using **FastAPI** and exposes RESTful endpoints for prediction and monitoring.

## Base URL
Public Entry Point (via Ingress): `http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/api`

## Endpoints

### 1. Predict Heart Disease
Generates a prediction based on patient clinical data.

- **URL**: `/predict`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Body (JSON)
| Field | Type | Description |
|-------|------|-------------|
| `age` | int | Age in years |
| `sex` | int | 1 = male, 0 = female |
| `cp` | int | Chest pain type (0-3) |
| `trestbps` | int | Resting blood pressure |
| `chol` | int | Serum cholestoral in mg/dl |
| `fbs` | int | Fasting blood sugar > 120 mg/dl (1 = true) |
| `restecg` | int | Resting electrocardiographic results |
| `thalach` | int | Maximum heart rate achieved |
| `exang` | int | Exercise induced angina (1 = yes) |
| `oldpeak` | float | ST depression induced by exercise |
| `slope` | int | Slope of the peak exercise ST segment |
| `ca` | int | Number of major vessels (0-3) |
| `thal` | int | Thalassemia (1 = normal, 2 = fixed defect, etc.) |

**Example Request:**
```json
{
  "age": 63,
  "sex": 1,
  "cp": 3,
  "trestbps": 145,
  "chol": 233,
  "fbs": 1,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 2.3,
  "slope": 0,
  "ca": 0,
  "thal": 1
}
```

#### Response (JSON)
| Field | Type | Description |
|-------|------|-------------|
| `prediction` | int | 0 = Normal, 1 = Heart Disease |
| `confidence` | float | Probability score (0.0 - 1.0) |

**Example Response:**
```json
{
  "prediction": 1,
  "confidence": 0.89
}
```

### 2. Interactive Documentation (Swagger UI)
FastAPI automatically generates interactive Swagger documentation.
- **URL**: `/docs` (Full path: `http://.../api/docs`)
- **Use Case**: Test API endpoints directly from the browser.

### 3. Health Check
Checks if the API is running.
- **URL**: `/`
- **Method**: `GET`
- **Response**: `"API is running"`

### 4. Metrics
Exposes Prometheus metrics.
- **URL**: `/metrics`
- **Method**: `GET`
- **Response**: Plain text Prometheus format.
