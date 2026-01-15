# DevOps Project API

A production-ready Flask REST API with complete DevOps pipeline including Docker, Kubernetes, CI/CD, security scanning, and monitoring.

## 🚀 Features

- **RESTful API** built with Flask
- **Structured JSON logging** with request tracing
- **Prometheus metrics** for monitoring
- **Docker & Docker Compose** for containerization
- **Kubernetes deployment** with ConfigMaps, health checks, and resource limits
- **CI/CD Pipeline** with GitHub Actions
- **Security scanning** (SAST with Bandit, DAST with OWASP ZAP)
- **Automated Docker image builds** and push to Docker Hub
- **CORS enabled** for cross-origin requests

## 📋 Prerequisites

- Python 3.11+
- Docker Desktop
- Kubernetes (Minikube or Docker Desktop Kubernetes)
- kubectl CLI
- Git

## 🏗️ Architecture

```
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Production Docker image
├── docker-compose.yml    # Local development setup
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # CI/CD pipeline
└── k8s/                  # Kubernetes manifests
    ├── namespace.yaml
    ├── configmap.yaml
    ├── deployment.yaml
    └── service.yaml
```

## 🛠️ Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/touka-lamouchi/devops-project-api.git
   cd devops-project-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

   API will be available at `http://localhost:5000`

### Docker

1. **Build the image**
   ```bash
   docker build -t devops-api .
   ```

2. **Run with Docker**
   ```bash
   docker run -d -p 5000:5000 devops-api
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

## ☸️ Kubernetes Deployment

### Prerequisites
Start Minikube:
```bash
minikube start --driver=docker
```

### Deploy to Kubernetes

1. **Apply all Kubernetes manifests**
   ```bash
   kubectl apply -f k8s/
   ```

2. **Verify deployment**
   ```bash
   kubectl get all -n devops-api
   ```

3. **Access the API**
   ```bash
   kubectl port-forward -n devops-api service/devops-api-service 8080:80
   ```
   
   API available at `http://localhost:8080`

### Kubernetes Resources

- **Namespace**: `devops-api` - Isolated environment
- **ConfigMap**: `devops-api-config` - Environment configuration
- **Deployment**: 3 replicas with health checks and resource limits
- **Service**: NodePort on port 30080

## 📡 API Endpoints

### Health Check
```bash
GET /health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-15T12:00:00",
  "service": "devops-project-api"
}
```

### Get All Items
```bash
GET /api/items
```
Response:
```json
{
  "items": [...],
  "count": 2
}
```

### Get Item by ID
```bash
GET /api/items/{id}
```

### Create Item
```bash
POST /api/items
Content-Type: application/json

{
  "name": "New Item",
  "description": "Item description"
}
```

### Update Item
```bash
PUT /api/items/{id}
Content-Type: application/json

{
  "name": "Updated Item",
  "description": "Updated description"
}
```

### Delete Item
```bash
DELETE /api/items/{id}
```

### Prometheus Metrics
```bash
GET /metrics
```
Returns Prometheus-formatted metrics including:
- HTTP request duration histograms
- Request counts by status code
- Python runtime metrics
- Memory and CPU usage

## 🔄 CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Build & Test** - Runs SAST security scan with Bandit
2. **Docker Build & Push** - Builds image and pushes to Docker Hub
3. **DAST Scan** - Runs OWASP ZAP security testing on deployed container

### Workflow Triggers
- Push to any branch
- Pull requests to main branch

### Artifacts
- Bandit security report (JSON)
- OWASP ZAP scan report (HTML)

## 🔒 Security

- **SAST**: Static analysis with Bandit
- **DAST**: Dynamic security testing with OWASP ZAP
- **Container scanning**: Automated on each build
- **No debug mode** in production
- **Resource limits** in Kubernetes

## 📊 Monitoring

### Prometheus Metrics
Access metrics at `/metrics` endpoint:
- Request latency (histogram)
- Request count by status code
- Python GC statistics
- Process memory and CPU usage

### Key Metrics
- `flask_http_request_duration_seconds` - Request duration
- `flask_http_request_total` - Total requests
- `process_resident_memory_bytes` - Memory usage
- `process_cpu_seconds_total` - CPU time

## 🧪 Testing

### Manual Testing
```bash
# Health check
curl http://localhost:5000/health

# Get items
curl http://localhost:5000/api/items

# Create item
curl -X POST http://localhost:5000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item","description":"Test"}'

# Metrics
curl http://localhost:5000/metrics
```

## 🐳 Docker Hub

Images are automatically published to:
```
toukalamouchi/devops-api:latest
toukalamouchi/devops-api:{git-sha}
```

Pull the image:
```bash
docker pull toukalamouchi/devops-api:latest
```

## 🔧 Configuration

### Environment Variables (ConfigMap)

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_ENV` | production | Flask environment |
| `FLASK_DEBUG` | false | Debug mode disabled |
| `APP_NAME` | DevOps Project API | Application name |
| `LOG_LEVEL` | INFO | Logging level |

### Resource Limits (Kubernetes)

| Resource | Request | Limit |
|----------|---------|-------|
| CPU | 100m | 500m |
| Memory | 128Mi | 256Mi |

## 📝 Logs

Structured JSON logging with request IDs:
```json
{
  "asctime": "2026-01-15 12:00:00",
  "name": "root",
  "levelname": "INFO",
  "message": "Fetching all items",
  "request_id": "abc-123-def"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## 👤 Author

**Touka Lamouchi**
- GitHub: [@touka-lamouchi](https://github.com/touka-lamouchi)
- Docker Hub: [toukalamouchi](https://hub.docker.com/u/toukalamouchi)

