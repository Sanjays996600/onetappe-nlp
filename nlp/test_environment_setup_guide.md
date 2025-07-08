# Test Environment Setup Guide for NLP Command System

## Overview

This document provides detailed instructions for setting up consistent test environments for the multilingual NLP command system. A properly configured test environment is essential for reliable, reproducible testing across development, testing, and production phases. This guide covers environment setup for different testing types, including unit, integration, performance, and security testing.

## Goals and Objectives

### Primary Goals

1. **Consistency**: Ensure consistent test environments across all testing phases
2. **Reproducibility**: Enable reproducible test results
3. **Isolation**: Provide isolated environments to prevent interference
4. **Efficiency**: Optimize environment setup for efficient testing
5. **Scalability**: Support scaling for performance and load testing

### Specific Objectives

1. Define environment requirements for each testing type
2. Provide setup instructions for local, CI/CD, and production-like environments
3. Establish environment validation procedures
4. Document environment management practices

## Environment Types

### 1. Development Environment

**Purpose**: Individual developer testing and debugging

**Characteristics**:
- Local setup on developer machines
- Quick feedback loop
- May use simplified dependencies
- Focused on unit and component testing

### 2. Continuous Integration Environment

**Purpose**: Automated testing in CI/CD pipeline

**Characteristics**:
- Automated setup and teardown
- Consistent across builds
- Optimized for test speed
- Supports unit, integration, and some system tests

### 3. Testing Environment

**Purpose**: Dedicated environment for QA testing

**Characteristics**:
- Stable configuration
- Similar to production
- Supports all test types
- Isolated from development and production

### 4. Performance Testing Environment

**Purpose**: Load, stress, and performance testing

**Characteristics**:
- Production-like configuration
- Scalable resources
- Monitoring instrumentation
- Isolated from other environments

### 5. Security Testing Environment

**Purpose**: Security testing and vulnerability assessment

**Characteristics**:
- Isolated network
- Production-like configuration
- Security monitoring tools
- Controlled access

## Environment Requirements

### 1. Hardware Requirements

#### Development Environment

- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 50+ GB SSD
- **Network**: Standard internet connection

#### CI/CD Environment

- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD
- **Network**: High-speed internet connection

#### Testing Environment

- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Storage**: 200+ GB SSD
- **Network**: High-speed internet connection

#### Performance Testing Environment

- **CPU**: 16+ cores
- **RAM**: 32+ GB
- **Storage**: 500+ GB SSD
- **Network**: High-speed, low-latency connection

### 2. Software Requirements

#### Operating System

- **Development**: macOS, Windows, or Linux
- **CI/CD**: Linux (Ubuntu 20.04 LTS or later)
- **Testing**: Linux (Ubuntu 20.04 LTS or later)
- **Performance**: Linux (Ubuntu 20.04 LTS or later)

#### Core Software

- **Python**: 3.8+ (3.9 recommended)
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.30+

#### Database

- **MongoDB**: 5.0+
- **Redis**: 6.2+

#### Message Broker

- **RabbitMQ**: 3.9+

#### NLP Libraries

- **spaCy**: 3.2+
- **NLTK**: 3.6+
- **Transformers**: 4.15+

#### Testing Tools

- **pytest**: 6.2+
- **pytest-cov**: 2.12+
- **pytest-mock**: 3.6+
- **pytest-xdist**: 2.5+
- **Locust**: 2.8+
- **OWASP ZAP**: 2.11+

#### Monitoring Tools

- **Prometheus**: 2.30+
- **Grafana**: 8.3+

### 3. Network Requirements

#### Connectivity

- **Development**: Internet access for package downloads
- **CI/CD**: Internet access for package downloads and service integration
- **Testing**: Controlled internet access
- **Performance**: Isolated network with controlled external access

#### Ports

- **API Server**: 8000
- **WhatsApp Integration**: 8001
- **MongoDB**: 27017
- **Redis**: 6379
- **RabbitMQ**: 5672, 15672 (management)
- **Prometheus**: 9090
- **Grafana**: 3000

#### Security

- **Firewall**: Restrict access to required ports only
- **TLS**: Enable for all external communications
- **VPN**: Required for remote access to testing environments

## Environment Setup Instructions

### 1. Development Environment Setup

#### Prerequisites

- Python 3.9
- Docker and Docker Compose
- Git

#### Setup Steps

1. **Clone Repository**

```bash
git clone https://github.com/your-org/nlp-command-system.git
cd nlp-command-system
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. **Download NLP Models**

```bash
python -m spacy download en_core_web_md
python -m spacy download hi_core_web_md
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
```

5. **Set Up Local Services**

```bash
docker-compose -f docker-compose.dev.yml up -d
```

6. **Configure Environment Variables**

Create a `.env` file in the project root:

```
ENVIRONMENT=development
MONGODB_URI=mongodb://localhost:27017/nlp_command_dev
REDIS_URI=redis://localhost:6379/0
RABBITMQ_URI=amqp://guest:guest@localhost:5672/
WHATSAPP_API_URL=http://localhost:8001/api/v1
WHATSAPP_API_KEY=dev_api_key
LOG_LEVEL=DEBUG
```

7. **Verify Setup**

```bash
python -m pytest tests/unit -v
```

### 2. CI/CD Environment Setup

#### GitHub Actions Configuration

Create `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:5.0
        ports:
          - 27017:27017
      redis:
        image: redis:6.2
        ports:
          - 6379:6379
      rabbitmq:
        image: rabbitmq:3.9-management
        ports:
          - 5672:5672
          - 15672:15672
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Download NLP models
      run: |
        python -m spacy download en_core_web_md
        python -m spacy download hi_core_web_md
        python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Test with pytest
      run: |
        pytest --cov=nlp tests/ --cov-report=xml
      env:
        ENVIRONMENT: ci
        MONGODB_URI: mongodb://localhost:27017/nlp_command_test
        REDIS_URI: redis://localhost:6379/1
        RABBITMQ_URI: amqp://guest:guest@localhost:5672/
        WHATSAPP_API_URL: http://localhost:8001/api/v1
        WHATSAPP_API_KEY: test_api_key
        LOG_LEVEL: INFO
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

### 3. Testing Environment Setup

#### Docker Compose Configuration

Create `docker-compose.test.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped
  
  redis:
    image: redis:6.2
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
  
  rabbitmq:
    image: rabbitmq:3.9-management
    ports:
      - "5672:5672"
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    restart: unless-stopped
  
  nlp_command_api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=testing
      - MONGODB_URI=mongodb://mongodb:27017/nlp_command_test
      - REDIS_URI=redis://redis:6379/0
      - RABBITMQ_URI=amqp://guest:guest@rabbitmq:5672/
      - WHATSAPP_API_URL=http://whatsapp_mock:8001/api/v1
      - WHATSAPP_API_KEY=test_api_key
      - LOG_LEVEL=INFO
    depends_on:
      - mongodb
      - redis
      - rabbitmq
      - whatsapp_mock
    restart: unless-stopped
  
  whatsapp_mock:
    build:
      context: ./whatsapp_mock
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - LOG_LEVEL=INFO
    restart: unless-stopped
  
  prometheus:
    image: prom/prometheus:v2.30.3
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped
  
  grafana:
    image: grafana/grafana:8.3.0
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  mongodb_data:
  redis_data:
  rabbitmq_data:
  prometheus_data:
  grafana_data:
```

#### Setup Steps

1. **Clone Repository**

```bash
git clone https://github.com/your-org/nlp-command-system.git
cd nlp-command-system
```

2. **Start Environment**

```bash
docker-compose -f docker-compose.test.yml up -d
```

3. **Load Test Data**

```bash
python scripts/load_test_data.py
```

4. **Run Tests**

```bash
python -m pytest tests/integration -v
```

### 4. Performance Testing Environment Setup

#### Docker Compose Configuration

Create `docker-compose.perf.yml`:

```yaml
version: '3.8'

services:
  # Include all services from docker-compose.test.yml
  # Add performance testing specific services
  
  locust-master:
    image: locustio/locust:2.8.3
    ports:
      - "8089:8089"
    volumes:
      - ./locust:/mnt/locust
    command: -f /mnt/locust/locustfile.py --master -H http://nlp_command_api:8000
    depends_on:
      - nlp_command_api
  
  locust-worker:
    image: locustio/locust:2.8.3
    volumes:
      - ./locust:/mnt/locust
    command: -f /mnt/locust/locustfile.py --worker --master-host locust-master
    depends_on:
      - locust-master
    deploy:
      replicas: 4
  
  node-exporter:
    image: prom/node-exporter:v1.3.1
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped
```

#### Locust Configuration

Create `locust/locustfile.py`:

```python
from locust import HttpUser, task, between
import random
import json

class NLPCommandUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between tasks
    
    def on_start(self):
        # Initialize user session
        self.user_id = f"user_{random.randint(1000, 9999)}"
        self.phone_number = f"+91{random.randint(7000000000, 9999999999)}"
    
    @task(10)
    def get_top_products_english(self):
        # Test get_top_products intent with English commands
        commands = [
            "show me top 5 products",
            "what are my best selling products",
            "top 10 products this week",
            "show best selling items this month",
            "top products last 30 days"
        ]
        command = random.choice(commands)
        
        payload = {
            "user_id": self.user_id,
            "phone_number": self.phone_number,
            "message": command,
            "timestamp": "2023-05-15T10:30:00Z"
        }
        
        self.client.post("/api/v1/process_command", json=payload)
    
    @task(5)
    def get_top_products_hindi(self):
        # Test get_top_products intent with Hindi commands
        commands = [
            "मुझे शीर्ष 5 उत्पाद दिखाएं",
            "मेरे सबसे अधिक बिकने वाले उत्पाद क्या हैं",
            "इस सप्ताह के शीर्ष 10 उत्पाद",
            "इस महीने के सबसे अधिक बिकने वाले आइटम दिखाएं",
            "पिछले 30 दिनों के शीर्ष उत्पाद"
        ]
        command = random.choice(commands)
        
        payload = {
            "user_id": self.user_id,
            "phone_number": self.phone_number,
            "message": command,
            "timestamp": "2023-05-15T10:30:00Z"
        }
        
        self.client.post("/api/v1/process_command", json=payload)
    
    @task(3)
    def get_orders_english(self):
        # Test get_orders intent with English commands
        commands = [
            "show me my recent orders",
            "get last 5 orders",
            "orders from last week",
            "show pending orders",
            "how many orders this month"
        ]
        command = random.choice(commands)
        
        payload = {
            "user_id": self.user_id,
            "phone_number": self.phone_number,
            "message": command,
            "timestamp": "2023-05-15T10:30:00Z"
        }
        
        self.client.post("/api/v1/process_command", json=payload)
    
    @task(2)
    def get_orders_hindi(self):
        # Test get_orders intent with Hindi commands
        commands = [
            "मुझे मेरे हाल के आदेश दिखाएं",
            "पिछले 5 आदेश प्राप्त करें",
            "पिछले सप्ताह के आदेश",
            "लंबित आदेश दिखाएं",
            "इस महीने कितने आदेश हैं"
        ]
        command = random.choice(commands)
        
        payload = {
            "user_id": self.user_id,
            "phone_number": self.phone_number,
            "message": command,
            "timestamp": "2023-05-15T10:30:00Z"
        }
        
        self.client.post("/api/v1/process_command", json=payload)
```

#### Setup Steps

1. **Clone Repository**

```bash
git clone https://github.com/your-org/nlp-command-system.git
cd nlp-command-system
```

2. **Start Environment**

```bash
docker-compose -f docker-compose.test.yml -f docker-compose.perf.yml up -d
```

3. **Load Test Data**

```bash
python scripts/load_performance_test_data.py
```

4. **Access Locust Web UI**

Open http://localhost:8089 in a web browser

5. **Start Performance Test**

Configure the test parameters in the Locust UI:
- Number of users: 100
- Spawn rate: 10 users per second
- Host: http://nlp_command_api:8000

6. **Monitor Performance**

Access Grafana at http://localhost:3000 to monitor system performance

### 5. Security Testing Environment Setup

#### Docker Compose Configuration

Create `docker-compose.security.yml`:

```yaml
version: '3.8'

services:
  # Include all services from docker-compose.test.yml
  # Add security testing specific services
  
  zap:
    image: owasp/zap2docker-stable:2.11.1
    ports:
      - "8080:8080"
      - "8090:8090"
    volumes:
      - ./zap:/zap/wrk
    command: zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true
  
  dependency-check:
    image: owasp/dependency-check:latest
    volumes:
      - .:/src
      - dependency-check-data:/usr/share/dependency-check/data
    command: --scan /src --format "ALL" --out /src/reports --suppression /src/suppression.xml

volumes:
  dependency-check-data:
```

#### ZAP Configuration

Create `zap/zap-baseline.conf`:

```properties
# ZAP Baseline Configuration

# General
zap.autorun=true

# Spider
spider.maxDepth=5
spider.threadCount=5

# Active Scan
activeScan.strength=high
activeScan.threadPerHost=5

# Reporting
report.outputFormat=html,xml,json
report.outputDir=/zap/wrk/reports
```

#### Setup Steps

1. **Clone Repository**

```bash
git clone https://github.com/your-org/nlp-command-system.git
cd nlp-command-system
```

2. **Start Environment**

```bash
docker-compose -f docker-compose.test.yml -f docker-compose.security.yml up -d
```

3. **Run ZAP Baseline Scan**

```bash
docker-compose -f docker-compose.security.yml run --rm zap zap-baseline.py -t http://nlp_command_api:8000 -c zap-baseline.conf
```

4. **Run Dependency Check**

```bash
docker-compose -f docker-compose.security.yml run --rm dependency-check
```

5. **View Reports**

Reports will be available in the `reports` directory

## Environment Validation

### 1. Validation Checklist

#### Development Environment

- [ ] Python version is 3.9+
- [ ] All required packages are installed
- [ ] NLP models are downloaded
- [ ] Local services (MongoDB, Redis, RabbitMQ) are running
- [ ] Environment variables are set correctly
- [ ] Unit tests pass

#### CI/CD Environment

- [ ] GitHub Actions workflow runs successfully
- [ ] All services start correctly
- [ ] All tests pass
- [ ] Code coverage is reported

#### Testing Environment

- [ ] All services are running
- [ ] Test data is loaded
- [ ] API endpoints are accessible
- [ ] Integration tests pass
- [ ] Monitoring tools are accessible

#### Performance Testing Environment

- [ ] All services are running with sufficient resources
- [ ] Locust is accessible and can run tests
- [ ] Monitoring tools show performance metrics
- [ ] System can handle expected load

#### Security Testing Environment

- [ ] ZAP is accessible and can scan the API
- [ ] Dependency check runs successfully
- [ ] Security reports are generated

### 2. Validation Scripts

#### Development Environment Validation

Create `scripts/validate_dev_env.py`:

```python
#!/usr/bin/env python3
import sys
import subprocess
import requests
import pymongo
import redis
import pika
import spacy
import nltk

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python version {version.major}.{version.minor}.{version.micro} OK")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor}.{version.micro} not supported. Need 3.8+")
        return False

def check_packages():
    print("Checking required packages...")
    required_packages = [
        "pytest", "pytest-cov", "pytest-mock", "pytest-xdist",
        "spacy", "nltk", "transformers",
        "pymongo", "redis", "pika"
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            all_installed = False
    
    return all_installed

def check_nlp_models():
    print("Checking NLP models...")
    models_ok = True
    
    # Check spaCy models
    try:
        spacy.load("en_core_web_md")
        print("✅ spaCy English model installed")
    except IOError:
        print("❌ spaCy English model not installed")
        models_ok = False
    
    try:
        spacy.load("hi_core_web_md")
        print("✅ spaCy Hindi model installed")
    except IOError:
        print("❌ spaCy Hindi model not installed")
        models_ok = False
    
    # Check NLTK data
    if "punkt" in nltk.data.path:
        print("✅ NLTK punkt installed")
    else:
        print("❌ NLTK punkt not installed")
        models_ok = False
    
    if "wordnet" in nltk.data.path:
        print("✅ NLTK wordnet installed")
    else:
        print("❌ NLTK wordnet not installed")
        models_ok = False
    
    return models_ok

def check_services():
    print("Checking services...")
    services_ok = True
    
    # Check MongoDB
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is running")
    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ MongoDB is not running")
        services_ok = False
    
    # Check Redis
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()
        print("✅ Redis is running")
    except redis.exceptions.ConnectionError:
        print("❌ Redis is not running")
        services_ok = False
    
    # Check RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        connection.close()
        print("✅ RabbitMQ is running")
    except pika.exceptions.AMQPConnectionError:
        print("❌ RabbitMQ is not running")
        services_ok = False
    
    return services_ok

def run_unit_tests():
    print("Running unit tests...")
    result = subprocess.run(["python", "-m", "pytest", "tests/unit", "-v"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Unit tests passed")
        return True
    else:
        print("❌ Unit tests failed")
        print(result.stdout)
        return False

def main():
    print("Validating development environment...\n")
    
    checks = [
        check_python_version(),
        check_packages(),
        check_nlp_models(),
        check_services(),
        run_unit_tests()
    ]
    
    if all(checks):
        print("\n✅ Development environment is valid!")
        return 0
    else:
        print("\n❌ Development environment validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

#### Testing Environment Validation

Create `scripts/validate_test_env.py`:

```python
#!/usr/bin/env python3
import sys
import requests
import time
import json

def check_api_health():
    print("Checking API health...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200 and response.json()["status"] == "ok":
            print("✅ API is healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code} {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API is not accessible")
        return False

def check_whatsapp_mock():
    print("Checking WhatsApp mock service...")
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200 and response.json()["status"] == "ok":
            print("✅ WhatsApp mock is healthy")
            return True
        else:
            print(f"❌ WhatsApp mock health check failed: {response.status_code} {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ WhatsApp mock is not accessible")
        return False

def check_monitoring_tools():
    print("Checking monitoring tools...")
    monitoring_ok = True
    
    # Check Prometheus
    try:
        response = requests.get("http://localhost:9090/-/healthy")
        if response.status_code == 200:
            print("✅ Prometheus is healthy")
        else:
            print(f"❌ Prometheus health check failed: {response.status_code} {response.text}")
            monitoring_ok = False
    except requests.exceptions.ConnectionError:
        print("❌ Prometheus is not accessible")
        monitoring_ok = False
    
    # Check Grafana
    try:
        response = requests.get("http://localhost:3000/api/health")
        if response.status_code == 200 and response.json()["database"] == "ok":
            print("✅ Grafana is healthy")
        else:
            print(f"❌ Grafana health check failed: {response.status_code} {response.text}")
            monitoring_ok = False
    except requests.exceptions.ConnectionError:
        print("❌ Grafana is not accessible")
        monitoring_ok = False
    
    return monitoring_ok

def test_command_processing():
    print("Testing command processing...")
    
    # Test English command
    english_payload = {
        "user_id": "test_user",
        "phone_number": "+919876543210",
        "message": "show me top 5 products",
        "timestamp": "2023-05-15T10:30:00Z"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/v1/process_command", json=english_payload)
        if response.status_code == 200 and "top products" in response.json()["response"].lower():
            print("✅ English command processing works")
            english_ok = True
        else:
            print(f"❌ English command processing failed: {response.status_code} {response.text}")
            english_ok = False
    except requests.exceptions.ConnectionError:
        print("❌ API is not accessible for English command")
        english_ok = False
    
    # Test Hindi command
    hindi_payload = {
        "user_id": "test_user",
        "phone_number": "+919876543210",
        "message": "मुझे शीर्ष 5 उत्पाद दिखाएं",
        "timestamp": "2023-05-15T10:30:00Z"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/v1/process_command", json=hindi_payload)
        if response.status_code == 200:
            print("✅ Hindi command processing works")
            hindi_ok = True
        else:
            print(f"❌ Hindi command processing failed: {response.status_code} {response.text}")
            hindi_ok = False
    except requests.exceptions.ConnectionError:
        print("❌ API is not accessible for Hindi command")
        hindi_ok = False
    
    return english_ok and hindi_ok

def main():
    print("Validating testing environment...\n")
    
    # Wait for services to be fully up
    print("Waiting for services to start...")
    time.sleep(10)
    
    checks = [
        check_api_health(),
        check_whatsapp_mock(),
        check_monitoring_tools(),
        test_command_processing()
    ]
    
    if all(checks):
        print("\n✅ Testing environment is valid!")
        return 0
    else:
        print("\n❌ Testing environment validation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## Environment Management

### 1. Environment Provisioning

#### Local Environment

```bash
# Clone repository
git clone https://github.com/your-org/nlp-command-system.git
cd nlp-command-system

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Download NLP models
python -m spacy download en_core_web_md
python -m spacy download hi_core_web_md
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"

# Start local services
docker-compose -f docker-compose.dev.yml up -d

# Validate environment
python scripts/validate_dev_env.py
```

#### Cloud Environment (AWS)

```bash
# Provision infrastructure using Terraform
cd terraform
terraform init
terraform apply -var-file=testing.tfvars

# Deploy application
cd ..
./scripts/deploy.sh testing

# Validate environment
./scripts/validate_env.sh testing
```

### 2. Environment Maintenance

#### Updating Dependencies

```bash
# Update Python packages
pip install -U -r requirements.txt
pip install -U -r requirements-dev.txt

# Update NLP models
python -m spacy download --force en_core_web_md
python -m spacy download --force hi_core_web_md

# Update Docker images
docker-compose -f docker-compose.dev.yml pull
docker-compose -f docker-compose.dev.yml up -d
```

#### Database Maintenance

```bash
# Backup MongoDB data
docker exec -it nlp-command-system_mongodb_1 mongodump --out /data/backup

# Restore MongoDB data
docker exec -it nlp-command-system_mongodb_1 mongorestore /data/backup

# Clear test data
python scripts/clear_test_data.py
```

### 3. Environment Monitoring

#### Prometheus Configuration

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'nlp_command_api'
    static_configs:
      - targets: ['nlp_command_api:8000']
  
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

#### Grafana Dashboard

Create a dashboard with the following panels:

1. **API Health**: Status of API endpoints
2. **Response Time**: Average and 90th percentile response time
3. **Throughput**: Requests per second
4. **Error Rate**: Percentage of requests resulting in errors
5. **Resource Usage**: CPU, memory, and disk usage
6. **Database Metrics**: MongoDB operations and latency

## Best Practices

### 1. Environment Isolation

- Use separate environments for development, testing, and production
- Isolate environments using Docker containers or virtual machines
- Use different database instances for each environment
- Implement network isolation between environments

### 2. Configuration Management

- Use environment variables for configuration
- Store sensitive information in secure vaults (e.g., AWS Secrets Manager)
- Use configuration files for environment-specific settings
- Implement configuration validation

### 3. Data Management

- Use test data generators for consistent test data
- Implement data cleanup procedures
- Backup and restore procedures for test data
- Sanitize production data before using in test environments

### 4. Resource Management

- Allocate appropriate resources for each environment
- Implement auto-scaling for performance testing
- Monitor resource usage and optimize
- Clean up unused resources

### 5. Security

- Implement least privilege access control
- Use secure communication (TLS)
- Regularly update dependencies
- Scan for vulnerabilities
- Implement secure coding practices

## Troubleshooting

### 1. Common Issues

#### API Not Accessible

**Symptoms**: Cannot connect to API endpoints

**Possible Causes**:
- Service not running
- Network configuration issue
- Port conflict

**Resolution**:
```bash
# Check if service is running
docker-compose ps

# Check logs
docker-compose logs nlp_command_api

# Restart service
docker-compose restart nlp_command_api
```

#### Database Connection Issues

**Symptoms**: API logs show database connection errors

**Possible Causes**:
- MongoDB not running
- Incorrect connection string
- Authentication issues

**Resolution**:
```bash
# Check if MongoDB is running
docker-compose ps mongodb

# Check MongoDB logs
docker-compose logs mongodb

# Verify connection string
echo $MONGODB_URI

# Restart MongoDB
docker-compose restart mongodb
```

#### NLP Model Loading Issues

**Symptoms**: API logs show errors loading NLP models

**Possible Causes**:
- Models not downloaded
- Incorrect model path
- Insufficient memory

**Resolution**:
```bash
# Download models again
python -m spacy download --force en_core_web_md
python -m spacy download --force hi_core_web_md

# Check model path
python -c "import spacy; print(spacy.util.get_data_path())"

# Increase container memory
# Edit docker-compose.yml to add memory limits
```

### 2. Debugging Tools

#### API Debugging

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Restart API with debug mode
docker-compose restart nlp_command_api

# View logs
docker-compose logs -f nlp_command_api
```

#### Database Debugging

```bash
# Connect to MongoDB shell
docker exec -it nlp-command-system_mongodb_1 mongo

# Check database status
db.serverStatus()

# Check collections
show collections
```

#### Network Debugging

```bash
# Check network connectivity
docker exec -it nlp-command-system_nlp_command_api_1 ping mongodb

# Check port availability
docker exec -it nlp-command-system_nlp_command_api_1 nc -zv mongodb 27017
```

## Conclusion

This test environment setup guide provides comprehensive instructions for setting up consistent, reliable test environments for the multilingual NLP command system. By following these guidelines, you can ensure that your testing environments are properly configured, validated, and maintained, leading to more reliable test results and higher quality software.

Remember to regularly update and maintain your test environments to ensure they remain consistent with your development and production environments. Proper environment management is a critical aspect of effective testing and quality assurance.

## Appendices

### Appendix A: Environment Variables Reference

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| ENVIRONMENT | Environment name (development, testing, production) | development | Yes |
| MONGODB_URI | MongoDB connection string | mongodb://localhost:27017/nlp_command_dev | Yes |
| REDIS_URI | Redis connection string | redis://localhost:6379/0 | Yes |
| RABBITMQ_URI | RabbitMQ connection string | amqp://guest:guest@localhost:5672/ | Yes |
| WHATSAPP_API_URL | WhatsApp API URL | http://localhost:8001/api/v1 | Yes |
| WHATSAPP_API_KEY | WhatsApp API key | dev_api_key | Yes |
| LOG_LEVEL | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO | No |
| API_PORT | API server port | 8000 | No |
| WORKERS | Number of worker processes | 4 | No |
| TIMEOUT | Request timeout in seconds | 30 | No |
| MAX_REQUESTS | Maximum requests per worker | 1000 | No |
| ENABLE_METRICS | Enable Prometheus metrics | true | No |

### Appendix B: Docker Compose Reference

#### Development Environment

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
  
  redis:
    image: redis:6.2
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  rabbitmq:
    image: rabbitmq:3.9-management
    ports:
      - "5672:5672"
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

volumes:
  mongodb_data:
  redis_data:
  rabbitmq_data:
```

### Appendix C: CI/CD Pipeline Reference

#### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 black isort
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    - name: Check formatting with black
      run: |
        black --check .
    - name: Check imports with isort
      run: |
        isort --check-only --profile black .
  
  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      mongodb:
        image: mongo:5.0
        ports:
          - 27017:27017
      redis:
        image: redis:6.2
        ports:
          - 6379:6379
      rabbitmq:
        image: rabbitmq:3.9-management
        ports:
          - 5672:5672
          - 15672:15672
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: Download NLP models
      run: |
        python -m spacy download en_core_web_md
        python -m spacy download hi_core_web_md
        python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
    - name: Test with pytest
      run: |
        pytest --cov=nlp tests/ --cov-report=xml
      env:
        ENVIRONMENT: ci
        MONGODB_URI: mongodb://localhost:27017/nlp_command_test
        REDIS_URI: redis://localhost:6379/1
        RABBITMQ_URI: amqp://guest:guest@localhost:5672/
        WHATSAPP_API_URL: http://localhost:8001/api/v1
        WHATSAPP_API_KEY: test_api_key
        LOG_LEVEL: INFO
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
  
  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop')
    steps:
    - uses: actions/checkout@v2
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    - name: Login to DockerHub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: yourorg/nlp-command-system:latest
  
  deploy-dev:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/develop'
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to development
      run: |
        echo "Deploying to development environment"
        # Add deployment script here
  
  deploy-prod:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to production
      run: |
        echo "Deploying to production environment"
        # Add deployment script here
```

### Appendix D: Resource Requirements

#### Minimum Requirements

| Environment | CPU | RAM | Storage | Network |
|-------------|-----|-----|---------|--------|
| Development | 4 cores | 8 GB | 50 GB SSD | Standard |
| CI/CD | 8 cores | 16 GB | 100 GB SSD | High-speed |
| Testing | 8 cores | 16 GB | 200 GB SSD | High-speed |
| Performance | 16 cores | 32 GB | 500 GB SSD | High-speed, low-latency |
| Security | 8 cores | 16 GB | 200 GB SSD | Isolated |

#### Recommended Requirements

| Environment | CPU | RAM | Storage | Network |
|-------------|-----|-----|---------|--------|
| Development | 8 cores | 16 GB | 100 GB SSD | Standard |
| CI/CD | 16 cores | 32 GB | 200 GB SSD | High-speed |
| Testing | 16 cores | 32 GB | 500 GB SSD | High-speed |
| Performance | 32 cores | 64 GB | 1 TB SSD | High-speed, low-latency |
| Security | 16 cores | 32 GB | 500 GB SSD | Isolated |