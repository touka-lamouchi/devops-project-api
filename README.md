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
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Production Docker image
├── docker-compose.yml              # Local development setup
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # CI/CD pipeline
└── k8s/                           # Kubernetes manifests
    ├── namespace.yaml             # Namespace isolation
    ├── configmap.yaml             # App configuration
    ├── deployment.yaml            # API deployment
    ├── service.yaml               # API service
    ├── prometheus-config.yaml     # Prometheus config
    ├── prometheus-deployment.yaml # Prometheus deployment
    ├── prometheus-service.yaml    # Prometheus service
    ├── grafana-deployment.yaml    # Grafana deployment
    └── grafana-service.yaml       # Grafana service
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

## 📊 Monitoring & Observability

### Prometheus + Grafana Stack

The project includes a complete monitoring stack deployed in Kubernetes:

**Prometheus** - Metrics collection and storage
- Automatically scrapes `/metrics` from the API every 15 seconds
- Access: `kubectl port-forward -n devops-api service/prometheus 9090:9090`
- URL: `http://localhost:9090`

**Grafana** - Metrics visualization and dashboards
- Pre-configured to use Prometheus as data source
- Access: `kubectl port-forward -n devops-api service/grafana 3000:3000`
- URL: `http://localhost:3000`
- Default credentials: `admin` / `admin`

### Available Metrics

Access raw metrics at `/metrics` endpoint:
- `flask_http_request_duration_seconds` - Request duration histogram
- `flask_http_request_total` - Total requests by status code
- `process_resident_memory_bytes` - Memory usage
- `process_cpu_seconds_total` - CPU time
- `python_gc_*` - Python garbage collection stats

### Setting up Grafana Dashboard

#### Access Grafana (Windows with Minikube)

1. **Start Grafana service** (keep terminal open):
   ```bash
   minikube service grafana -n devops-api
   ```
   This will output a URL like `http://127.0.0.1:XXXXX`

2. **Open Grafana** in your browser using the provided URL
3. **Login** with default credentials: `admin` / `admin`

#### Add Prometheus Data Source

1. Click **☰** menu → **Connections** → **Data sources**
2. Click **"Add data source"**
3. Select **"Prometheus"**
4. Configure:
   - **URL**: `http://prometheus:9090`
   - Leave other settings as default
5. Click **"Save & Test"** - should show green ✓

#### Create Monitoring Dashboard

1. Click **☰** → **Dashboards** → **New** → **New Dashboard**
2. Click **"+ Add visualization"** → Select **"prometheus"**

#### Panel 1: Total Requests (Stat)
- **Query**: `sum(flask_http_request_duration_seconds_count)`
- **Title**: `Total Requests`
- **Visualization**: Stat
- Click **Apply**

#### Panel 2: API Request Rate (Time Series)
- **Query**: `sum by (path) (rate(flask_http_request_duration_seconds_count[1m]))`
- **Title**: `API Request Rate`
- **Visualization**: Time series
- **Unit**: requests/sec (reqps)
- **Style**: Lines
- Click **Apply**

#### Panel 3: Requests by Endpoint (Pie Chart)
- **Query**: `sum by (path) (flask_http_request_duration_seconds_count)`
- **Title**: `Requests by Endpoint`
- **Visualization**: Pie chart
- **Labels**: Name and Value
- **Legend**: Show with values and percentages
- Click **Apply**

#### Panel 4: Response Time (Time Series)
- **Query**: `rate(flask_http_request_duration_seconds_sum[1m]) / rate(flask_http_request_duration_seconds_count[1m])`
- **Title**: `Average Response Time`
- **Visualization**: Time series
- **Unit**: seconds (s)
- Click **Apply**

5. **Save Dashboard**: Click 💾 icon → Name: `DevOps API Monitoring` → **Save**

### Important Notes

**Path Labels in Metrics**: The Flask app uses `PrometheusMetrics(app, group_by='path')` to track metrics by endpoint. This allows splitting data by `/health`, `/api/items`, etc.

**Correct Metrics to Use**:
- ✅ Use: `flask_http_request_duration_seconds_count` (has path labels)
- ❌ Avoid: `flask_http_request_total` (no path labels)

**Generate Test Traffic** (for visualization):
```bash
# Access API service
minikube service devops-api-service -n devops-api

# Generate requests (in new terminal)
for ($i=1; $i -le 30; $i++) {
    Invoke-WebRequest http://127.0.0.1:PORT/health -UseBasicParsing
    Invoke-WebRequest http://127.0.0.1:PORT/api/items -UseBasicParsing
}
```

### Troubleshooting Grafana

**"Failed to fetch" error**:
- The `minikube service` terminal must stay open for port forwarding
- Restart: `minikube service grafana -n devops-api`

**Grafana ImagePullBackOff**:
- Minikube may have slow/no internet access
- Solution: Pre-load image
  ```bash
  docker pull grafana/grafana:latest
  minikube image load grafana/grafana:latest
  kubectl rollout restart deployment/grafana -n devops-api
  ```

**No data in dashboards**:
- Wait 15-30 seconds for Prometheus to scrape metrics
- Generate traffic to API endpoints
- Verify Prometheus is scraping: `minikube service prometheus -n devops-api` → Status → Targets

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

