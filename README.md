# AI-Powered Worker Productivity Dashboard

A full-stack web application that ingests AI-generated events from CCTV systems and displays real-time productivity metrics for factory workers and workstations.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-18.2-blue)

## 🏗️ Architecture Overview

### High-Level Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   AI CCTV Edge  │      │   Backend API    │      │    Frontend     │
│    Devices      │─────▶│   (FastAPI)      │◀─────│   Dashboard     │
│  (CV Systems)   │ JSON │                  │ REST │    (React)      │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  SQLite Database │
                         │  (Events, Stats) │
                         └──────────────────┘
```

### Component Details

#### 1. **Edge Layer (AI CCTV Systems)**
- Computer vision models process video streams
- Generate structured event data (working, idle, product_count, etc.)
- Send events to backend API via HTTP/HTTPS
- Support for batching to handle intermittent connectivity

#### 2. **Backend Layer (FastAPI)**
- RESTful API for event ingestion and metrics retrieval
- SQLite database for data persistence
- Real-time metrics computation engine
- Duplicate detection and out-of-order event handling
- Admin endpoints for data management

#### 3. **Frontend Layer (React)**
- Real-time dashboard displaying factory, worker, and workstation metrics
- Filtering and drill-down capabilities
- Responsive design for various screen sizes
- Auto-refresh functionality

## 📊 Database Schema

```sql
-- Workers Table
CREATE TABLE workers (
    worker_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workstations Table
CREATE TABLE workstations (
    station_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events Table
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    worker_id TEXT,
    workstation_id TEXT,
    event_type TEXT NOT NULL,  -- 'working', 'idle', 'absent', 'product_count'
    confidence REAL,
    count INTEGER DEFAULT 0,   -- For production counting
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (worker_id) REFERENCES workers(worker_id),
    FOREIGN KEY (workstation_id) REFERENCES workstations(station_id)
);

-- Indexes for Performance
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_events_worker ON events(worker_id);
CREATE INDEX idx_events_workstation ON events(workstation_id);
CREATE INDEX idx_events_type ON events(event_type);
```

## 📈 Metric Definitions

### Worker-Level Metrics

| Metric | Definition | Calculation Method |
|--------|------------|-------------------|
| **Total Active Time** | Hours spent in "working" state | Sum of durations between consecutive events where event_type='working' |
| **Total Idle Time** | Hours spent in "idle" state | Sum of durations between consecutive events where event_type='idle' |
| **Utilization %** | Percentage of time actively working | (Total Active Time / (Total Active Time + Total Idle Time)) × 100 |
| **Total Units Produced** | Number of units produced | Sum of count field where event_type='product_count' |
| **Units per Hour** | Production rate | Total Units Produced / Total Active Time |

### Workstation-Level Metrics

| Metric | Definition | Calculation Method |
|--------|------------|-------------------|
| **Occupancy Time** | Hours workstation was actively used | Sum of durations for all 'working' events at this station |
| **Utilization %** | Percentage of observed time that station was occupied | (Occupancy Time / Total Observation Time) × 100 |
| **Total Units Produced** | Units produced at this station | Sum of count where event_type='product_count' for this station |
| **Throughput Rate** | Production rate at station | Total Units Produced / Occupancy Time |

### Factory-Level Metrics

| Metric | Definition | Calculation Method |
|--------|------------|-------------------|
| **Total Productive Time** | Cumulative working hours across all workers | Sum of all workers' Total Active Time |
| **Total Production Count** | Total units produced factory-wide | Sum of all product_count events |
| **Average Production Rate** | Overall factory production efficiency | Total Production Count / Total Productive Time |
| **Average Utilization** | Mean worker utilization | Average of all worker utilization percentages |

### Time Duration Calculation Assumptions

1. **Event Duration**: Each event represents the *start* of a state. Duration is calculated as the time until the next event.
2. **Last Event**: If no subsequent event exists, assume default duration of 10 minutes.
3. **Anomaly Handling**: Durations exceeding 2 hours are capped (handles overnight/weekend gaps).
4. **Production Events**: `product_count` events are instantaneous and don't contribute to time calculations.
5. **Out-of-Order Events**: Events are sorted by timestamp before processing, naturally handling out-of-order arrivals.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation & Running

```bash
# Clone the repository
git clone <repository-url>
cd AI-Powered-Worker-Productivity-Dashboard

# Start the application using Docker Compose
docker-compose up --build

# The application will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
```

The database will be automatically populated with 7 days of sample data on first run.

### Running Without Docker

#### Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.seed_data  # Initialize and seed database
python -m app.main       # Start FastAPI server
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Event Ingestion

```bash
# Ingest single event
POST /api/events
Content-Type: application/json

{
  "timestamp": "2026-01-15T10:15:00Z",
  "worker_id": "W1",
  "workstation_id": "S3",
  "event_type": "working",
  "confidence": 0.93,
  "count": 0
}

# Ingest batch of events (for intermittent connectivity)
POST /api/events/batch
Content-Type: application/json

[
  { /* event 1 */ },
  { /* event 2 */ }
]
```

### Metrics Retrieval

```bash
# Get complete dashboard data
GET /api/metrics/dashboard

# Get worker metrics (all or specific)
GET /api/metrics/workers
GET /api/metrics/workers?worker_id=W1

# Get workstation metrics (all or specific)
GET /api/metrics/workstations
GET /api/metrics/workstations?station_id=S3

# Get factory-level metrics
GET /api/metrics/factory
```

### Data Management

```bash
# Refresh dummy data (Admin)
POST /api/admin/seed-data?days=7

# Get database statistics
GET /api/admin/stats

# List all workers
GET /api/workers

# List all workstations
GET /api/workstations
 ## 🚀 Deployment
 
 ### Deploy to Render (Cloud Platform)
 
 This application is ready to deploy to [Render](https://render.com) with zero configuration.
 
 #### Quick Deploy
 1. **Push to GitHub**:
     ```bash
     git add .
     git commit -m "Deploy to Render"
     git push origin main
     ```
 
 2. **Deploy on Render**:
     - Go to [Render Dashboard](https://dashboard.render.com/)
     - Click "New" → "Blueprint"
     - Connect your repository
     - Click "Apply"
 
 3. **Access Your App**:
     - Frontend: `https://worker-productivity-frontend.onrender.com`
     - Backend: `https://worker-productivity-backend.onrender.com`
     - API Docs: `https://worker-productivity-backend.onrender.com/docs`
 
 #### What Gets Deployed
 
 ✅ **Backend** (Python Web Service):
 - FastAPI application
 - Automatic database initialization
 - Pre-loaded with sample data
 - Persistent disk for data storage
 
 ✅ **Frontend** (Static Site):
 - React dashboard
 - Optimized production build
 - CDN distribution
 
 #### Important Configuration
 
 After backend deploys, update frontend environment:
 1. Go to frontend service settings in Render
 2. Add environment variable:
     - Key: `VITE_API_URL`
     - Value: `https://worker-productivity-backend.onrender.com`
 3. Trigger manual deploy
 
 #### Free Tier Notes
 - Services sleep after 15 minutes of inactivity
 - First request may take 30-60 seconds (cold start)
 - Sufficient for development and testing
 
 📚 **For detailed deployment instructions, see [RENDER_DEPLOY.md](RENDER_DEPLOY.md)**
 
 📖 **For advanced deployment options, see [DEPLOYMENT.md](DEPLOYMENT.md)**
 
```

## 🛡️ Handling Edge Cases

### 1. Intermittent Connectivity

**Problem**: Edge devices may lose network connectivity temporarily.

**Solutions Implemented**:
- **Batch Event Ingestion**: `/api/events/batch` endpoint accepts multiple events in a single request
- **Edge-Side Queuing**: Edge devices should implement local buffering
- **Idempotent Operations**: Duplicate detection ensures events aren't processed twice
- **Resilient Architecture**: Events are stored persistently once received

**Recommended Edge Implementation**:
```python
# Pseudo-code for edge device
event_queue = []
retry_attempts = 0

while True:
    event = generate_event_from_cv()
    event_queue.append(event)
    
    if len(event_queue) >= BATCH_SIZE or time_since_last_send > INTERVAL:
        try:
            response = send_batch(event_queue)
            if response.status == 201:
                event_queue.clear()
                retry_attempts = 0
        except NetworkError:
            retry_attempts += 1
            wait_time = min(2 ** retry_attempts, MAX_BACKOFF)
            time.sleep(wait_time)
```

### 2. Duplicate Events

**Problem**: Network retries or system issues may cause duplicate event submissions.

**Solution Implemented**:
- **Composite Key Detection**: Events are considered duplicates if they have identical:
  - Timestamp
  - Worker ID
  - Workstation ID
  - Event Type
- **Graceful Handling**: Duplicates return status `duplicate` without raising errors
- **Database Constraints**: Prevents duplicate data insertion

**API Response for Duplicate**:
```json
{
  "status": "duplicate",
  "message": "Event already exists, skipping insertion"
}
```

### 3. Out-of-Order Timestamps

**Problem**: Network delays or asynchronous processing may cause events to arrive out of chronological order.

**Solutions Implemented**:
- **Accept All Events**: Backend accepts events regardless of arrival order
- **Sort Before Processing**: Metrics computation sorts events by timestamp before analysis
- **Indexed Timestamps**: Database index on timestamp field ensures efficient sorting
- **No Real-Time Dependency**: System doesn't assume sequential arrival

**Example**:
```
Arrival Order:    T3, T1, T4, T2
Processing Order: T1, T2, T3, T4  (sorted automatically)
```

## 🤖 ML Operations & Scalability

### Model Versioning

**Strategy**: Semantic versioning for CV models with metadata tracking

**Implementation Approach**:
```python
# Extended Event Schema
{
  "timestamp": "2026-01-15T10:15:00Z",
  "worker_id": "W1",
  "workstation_id": "S3",
  "event_type": "working",
  "confidence": 0.93,
  "count": 0,
  "model_version": "2.1.3",  # NEW: Track model version
  "model_name": "worker-activity-classifier"  # NEW: Model identifier
}

# Database Schema Addition
ALTER TABLE events ADD COLUMN model_version TEXT;
ALTER TABLE events ADD COLUMN model_name TEXT;
```

**Benefits**:
- Track which model version generated each prediction
- Correlate accuracy degradation with specific model versions
- Enable A/B testing between model versions
- Facilitate rollback to previous versions if issues arise

**Model Registry**:
```python
# models_registry.py
MODELS = {
    "worker-activity-classifier": {
        "versions": {
            "2.1.3": {
                "deployed_at": "2026-01-01",
                "accuracy": 0.94,
                "endpoint": "model-server-1.local"
            },
            "2.1.2": {
                "deployed_at": "2025-12-15",
                "accuracy": 0.92,
                "endpoint": "model-server-2.local"
            }
        },
        "active_version": "2.1.3"
    }
}
```

### Detecting Model Drift

**Drift Types**:
1. **Data Drift**: Input distribution changes (e.g., new workstation layouts)
2. **Concept Drift**: Relationship between inputs and outputs changes
3. **Performance Drift**: Model accuracy degrades over time

**Detection Methods**:

#### 1. Confidence Score Monitoring
```python
# Monitor average confidence scores over time
SELECT 
    DATE(timestamp) as date,
    model_version,
    AVG(confidence) as avg_confidence,
    STDDEV(confidence) as confidence_std
FROM events
WHERE event_type != 'product_count'
GROUP BY DATE(timestamp), model_version
ORDER BY date DESC;

# Alert if confidence drops below threshold
if avg_confidence < 0.80:
    trigger_drift_alert()
```

#### 2. Prediction Distribution Analysis
```python
# Monitor event type distribution
SELECT 
    event_type,
    COUNT(*) as count,
    AVG(confidence) as avg_confidence
FROM events
WHERE DATE(timestamp) = CURRENT_DATE
GROUP BY event_type;

# Compare with historical baseline
if abs(current_dist - baseline_dist) > THRESHOLD:
    flag_distribution_drift()
```

#### 3. Ground Truth Validation
```python
# Periodic manual labeling for validation
class DriftDetector:
    def detect_drift(self, validation_set):
        predictions = model.predict(validation_set)
        current_accuracy = calculate_accuracy(predictions, ground_truth)
        
        if current_accuracy < self.baseline_accuracy - 0.05:
            return True  # Significant drift detected
        return False
```

#### 4. Statistical Tests
- **Kolmogorov-Smirnov Test**: Compare feature distributions
- **PSI (Population Stability Index)**: Measure distribution shifts
- **Chi-Square Test**: Monitor categorical variable distributions

**Drift Monitoring Dashboard** (Future Enhancement):
```
+----------------------------------+
| Model Performance Monitor        |
+----------------------------------+
| Average Confidence (7d): 0.89    |
| Baseline: 0.93                   |
| Status: ⚠️  DRIFT DETECTED        |
|                                  |
| Event Distribution:              |
|   Working: 65% (Expected: 70%)   |
|   Idle: 25% (Expected: 20%)      |
|   Product: 10% (Expected: 10%)   |
+----------------------------------+
```

### Triggering Retraining

**Retraining Triggers**:

1. **Performance-Based**
   - Accuracy drops below threshold (e.g., < 85%)
   - Confidence scores decrease significantly
   - Error rate increases

2. **Time-Based**
   - Scheduled retraining (e.g., monthly)
   - After significant data accumulation

3. **Drift-Based**
   - Data distribution shift detected
   - New event patterns emerge

**Retraining Pipeline**:

```python
class RetrainingPipeline:
    def __init__(self):
        self.drift_detector = DriftDetector()
        self.performance_monitor = PerformanceMonitor()
        
    def should_retrain(self):
        """Decide if retraining is needed"""
        reasons = []
        
        # Check performance
        if self.performance_monitor.accuracy < 0.85:
            reasons.append("Low accuracy")
        
        # Check drift
        if self.drift_detector.detect_drift():
            reasons.append("Data drift detected")
        
        # Check time since last training
        if days_since_training > 30:
            reasons.append("Scheduled retraining")
        
        return len(reasons) > 0, reasons
    
    def trigger_retraining(self):
        """Initiate retraining workflow"""
        # 1. Extract fresh training data
        training_data = extract_recent_events(days=90)
        
        # 2. Add manual labels from validation set
        labeled_data = merge_with_ground_truth(training_data)
        
        # 3. Train new model
        new_model = train_model(labeled_data)
        
        # 4. Validate on holdout set
        validation_metrics = validate_model(new_model)
        
        # 5. If improved, deploy
        if validation_metrics.accuracy > current_model.accuracy:
            deploy_model(new_model, version="2.2.0")
        
        # 6. Monitor shadow deployment
        shadow_test(new_model, duration_hours=24)
```

**Automated Retraining Workflow**:
```
┌──────────────┐
│ Monitor Drift│
│  & Performance │
└───────┬──────┘
        │
        ▼
  ┌──────────┐
  │ Trigger? │──No──▶ Continue Monitoring
  └────┬─────┘
       │Yes
       ▼
┌─────────────┐
│Collect Data │
│& Labels     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Train New    │
│Model        │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Validate &   │
│A/B Test     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Deploy if    │
│Better       │
└─────────────┘
```

## 📈 Scaling Strategy

### From 5 Cameras → 100+ Cameras → Multi-Site

#### Phase 1: Small Scale (5-10 Cameras)
**Current Architecture** ✓
- Single server running backend + database
- SQLite sufficient for 10K-50K events/day
- Docker Compose on single machine
- Vertical scaling (add CPU/RAM)

**Capacity**: ~50K events/day, Single site

---

#### Phase 2: Medium Scale (10-100 Cameras)

**Required Changes**:

1. **Database Migration**
   ```
   SQLite → PostgreSQL
   ```
   - Better concurrent write handling
   - Connection pooling
   - Replication support

2. **Backend Scaling**
   ```
   Single Container → Multiple Backend Instances + Load Balancer
   ```
   ```yaml
   # docker-compose-scaled.yml
   services:
     backend:
       deploy:
         replicas: 5
     nginx:
       image: nginx:alpine
       # Load balance across backend instances
   ```

3. **Caching Layer**
   ```
   Add Redis for:
   - Metrics caching (reduce DB queries)
   - Rate limiting
   - Session management
   ```

4. **Message Queue**
   ```
   Add RabbitMQ/Kafka:
   - Decouple event ingestion from processing
   - Buffer spikes in event traffic
   - Retry failed processing
   ```

   ```
   Edge Devices → API Gateway → Message Queue → Workers → Database
                                      ↓
                                   Cache (Redis)
   ```

**Capacity**: ~500K events/day, Single site

---

#### Phase 3: Large Scale (100+ Cameras)

**Architecture Changes**:

1. **Microservices Decomposition**
   ```
   Monolithic API → Separate Services:
   - Event Ingestion Service
   - Metrics Computation Service
   - API Gateway
   - Worker Service
   - Workstation Service
   ```

2. **Database Sharding**
   ```python
   # Shard by site_id or date
   def get_shard(site_id):
       return f"db_shard_{site_id % NUM_SHARDS}"
   ```

3. **Time-Series Database**
   ```
   Add InfluxDB/TimescaleDB:
   - Optimized for time-series event data
   - Better compression
   - Efficient time-range queries
   ```

4. **Kubernetes Deployment**
   ```yaml
   # k8s deployment
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: ingestion-service
   spec:
     replicas: 20
     autoscaling:
       enabled: true
       minReplicas: 10
       maxReplicas: 50
       targetCPU: 70
   ```

5. **Edge Computing**
   ```
   Edge Devices do local processing:
   - Pre-filtering events
   - Local aggregation
   - Send only summaries to cloud
   ```

**Capacity**: 5M+ events/day, Single site

---

#### Phase 4: Multi-Site (Global Scale)

**Architecture**: Hierarchical/Federated

```
                   ┌─────────────────┐
                   │  Central Cloud  │
                   │  (Aggregated    │
                   │   Metrics)      │
                   └────────┬────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼─────┐      ┌────▼─────┐      ┌────▼─────┐
    │ Regional │      │ Regional │      │ Regional │
    │ Hub (US) │      │ Hub (EU) │      │ Hub (APAC)│
    └────┬─────┘      └────┬─────┘      └────┬─────┘
         │                 │                  │
      ┌──┴──┐           ┌──┴──┐           ┌──┴──┐
   Factory Factory   Factory Factory   Factory Factory
```

**Components**:

1. **Regional Hubs**
   - Process local factory data
   - Compute regional metrics
   - Sync to central cloud periodically

2. **Edge-First Architecture**
   ```
   Factory Edge → Regional Hub → Central Cloud
   (Real-time)     (Minutes)      (Hours/Daily)
   ```

3. **Data Residency**
   - Keep raw data at regional level (compliance)
   - Sync only aggregated metrics globally

4. **Multi-Tenancy**
   ```python
   # Tenant isolation
   @app.middleware("http")
   async def tenant_middleware(request: Request, call_next):
       tenant_id = get_tenant_from_header(request)
       set_tenant_context(tenant_id)
       response = await call_next(request)
       return response
   ```

5. **Disaster Recovery**
   - Multi-region replication
   - Automated failover
   - Backup and restore procedures

**Technology Stack Evolution**:

| Component | Small (5) | Medium (100) | Large (100+) | Multi-Site |
|-----------|-----------|--------------|--------------|------------|
| Backend | FastAPI | FastAPI | Microservices | Federated Services |
| Database | SQLite | PostgreSQL | Sharded PostgreSQL + TimescaleDB | Distributed DB (CockroachDB) |
| Queue | - | RabbitMQ | Kafka | Kafka (Global) |
| Cache | - | Redis | Redis Cluster | Redis + CDN |
| Orchestration | Docker Compose | Docker Swarm | Kubernetes | Multi-Region K8s |
| Monitoring | Logs | Prometheus | Full observability stack | Distributed tracing |

**Capacity**: 50M+ events/day, Global scale

---

### Cost Optimization

1. **Edge Processing**: Reduce data transfer costs
2. **Data Tiering**: Hot/Warm/Cold storage
3. **Serverless Functions**: For sporadic workloads
4. **Spot Instances**: For non-critical batch processing

## 🔍 Testing the Application

### Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/

# Get dashboard metrics
curl http://localhost:8000/api/metrics/dashboard

# Ingest a test event
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2026-03-02T10:30:00Z",
    "worker_id": "W1",
    "workstation_id": "S1",
    "event_type": "working",
    "confidence": 0.95,
    "count": 0
  }'

# Refresh dummy data
curl -X POST http://localhost:8000/api/admin/seed-data?days=7

# Get database stats
curl http://localhost:8000/api/admin/stats
```

## 📁 Project Structure

```
AI-Powered-Worker-Productivity-Dashboard/
│
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── database.py       # Database setup and connection
│   │   ├── models.py         # Pydantic models
│   │   ├── metrics.py        # Metrics computation logic
│   │   └── seed_data.py      # Data seeding utilities
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Backend container definition
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── api.js           # API client
│   │   ├── index.css        # Styles
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile           # Frontend container definition
│   └── .gitignore
│
├── docker-compose.yml       # Multi-container orchestration
└── README.md               # This file
```

## 🤝 Contributing

This is a technical assessment project. For improvements or questions, please contact the repository owner.

## 📄 License

This project is created for assessment purposes.

## 🎯 Assessment Completion Checklist

✅ **Functional Requirements**
- [x] 6 workers and 6 workstations with metadata
- [x] Backend APIs for event ingestion and metrics
- [x] Database schema with SQLite
- [x] Pre-populated dummy data
- [x] Worker-level metrics computation
- [x] Workstation-level metrics computation
- [x] Factory-level metrics computation
- [x] Frontend dashboard with all visualizations
- [x] Filtering capabilities
- [x] Data refresh via API

✅ **Technical Requirements**
- [x] Dockerized application
- [x] docker-compose setup
- [x] Run instructions
- [x] API documentation

✅ **Theoretical Questions**
- [x] Edge → Backend → Dashboard architecture explained
- [x] Handling intermittent connectivity
- [x] Duplicate event handling
- [x] Out-of-order timestamp handling
- [x] Model versioning strategy
- [x] Model drift detection approach
- [x] Retraining trigger methodology
- [x] Scaling strategy (5 → 100+ → multi-site)

---

**Built with ❤️  for factory productivity optimization**
