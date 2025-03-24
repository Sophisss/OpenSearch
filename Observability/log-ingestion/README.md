# OpenSearch Fake Log Generator: Simulating & Analyzing HTTP Logs

## 📌 Overview 
This script generates realistic HTTP logs and sends them to **OpenSearch** for **log analysis**, **observability**, and **monitoring**. 

It simulates various API requests, HTTP response statuses, and user behaviors, making it ideal for benchmarking, testing, and security analysis

## 🛠 Features
✔️ **Realistic log simulation** – Generates fake logs with structured data (IP addresses, user agents, timestamps, geolocation, HTTP methods, response codes). \
✔️ **Configurable execution** – Allows users to specify the number of logs and delay between them. \
✔️ **OpenSearch integration** – Logs are automatically indexed in OpenSearch for easy retrieval and analysis.

## 📂️ Requirements 

### Prerequisites
- **Python 3.8+**
- **OpenSearch cluster** (hosted or local instance)

### Install Dependencies
Ensure you have all the required Python packages installed:
  ```sh
    pip install -r requirements.txt
  ```

## ⚙️ Configuration

### OpenSearch Settings

Modify the following variables in `log_generator.py` to match your **Docker Compose setup**:

```python
OPENSEARCH_URL = "https://your-opensearch-instance:9200"  # Replace with your OpenSearch container hostname
INDEX_NAME = "logs-demo"
USERNAME = "your-admin-user"  # Use the OpenSearch username set in your configuration
PASSWORD = "your-password"  # Use the corresponding password
```

## 🔧 Usage
Run the script with customizable options:
  ```sh
    python log_generator.py --num 500 --sleep 0.2
   ```

### Command-line Arguments

| Argument     | Description                                  | Default |
|-------------|----------------------------------------------|---------|
| `--num`, `-n`  | Number of logs to generate (0 for infinite) | 100     |
| `--sleep`, `-s` | Delay between log entries (in seconds)    | 0.5     |


## 📊 Example Log Output

A generated log entry will be structured as follows:

```json
{
  "timestamp": "2025-03-22T14:32:10.123456Z",
  "ip": "192.168.1.100",
  "session_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "user_id": 1234,
  "http_method": "GET",
  "url": "/api/v1/orders/345",
  "status_code": 200,
  "response_size": 5043,
  "referer": "https://example.com",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
  "browser": "Chrome",
  "os": "Windows",
  "device_type": "Desktop",
  "request_time": 0.245
}
```

## 🔍 Viewing Logs in OpenSearch Dashboards
Once the logs are ingested into OpenSearch, you can visualize them using **OpenSearch Dashboards**:

### 1️⃣ Open OpenSearch Dashboards
If running locally, navigate to:

👉 https://localhost:5601 (or the URL specified in your Docker setup)

### 2️⃣ Navigate to Observability → Logs
- In the left sidebar, go to **Observability**
- Click on **Logs**

### 3️⃣ Open Event Explorer
- Click **Event Explorer** to build a custom query

### 4️⃣ Run a PPL Query
In the **Query Editor**, enter the following **Piped Processing Language (PPL)** query to filter logs from the correct index:

  ```ppl
    source = logs-demo
   ```

### 5️⃣ Visualize the Logs
- Click **Run** to execute the query
- Explore and analyze your logs in the results table

## 📈 Use Cases
Once logs are ingested into OpenSearch, they can be leveraged for multiple use cases: 

- **Log Analysis & Troubleshooting** – Identify errors, slow requests, and unusual traffic patterns.
- **Monitoring & Observability** - Visualize API metrics, track user activity, and set up alerts.
- **Security & Threat Detection** - Detect unauthorized access, DDoS attacks, and suspicious behavior.
- **Performance Benchmarking** - Analyze response times, optimize APIs, and simulate load testing.