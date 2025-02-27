#!/usr/bin/python
import time
import datetime
import random
import argparse
import requests
import numpy
from faker import Faker
from tzlocal import get_localzone
from urllib.parse import urlparse

# OpenSearch Configuration (UPDATE THIS)
OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "logs-demo"
USERNAME = "admin"
PASSWORD = "Str@ngPasword1!"

local = get_localzone()
faker = Faker()

# Command-line arguments
parser = argparse.ArgumentParser(description="Enhanced Fake Log Generator")
parser.add_argument("--num", "-n", dest='num_lines', help="Number of logs to generate (0 for infinite)", type=int,
                    default=100)
parser.add_argument("--sleep", "-s", help="Sleep time between logs (in seconds)", default=0.5, type=float)
args = parser.parse_args()

log_lines = args.num_lines if args.num_lines > 0 else float('inf')

response_codes = ["200", "404", "500", "301", "403", "503"]
http_methods = ["GET", "POST", "DELETE", "PUT", "PATCH"]
resources = ["/login", "/register", "/products", "/cart", "/checkout", "/api/v1/user", "/api/v1/orders",
             "/api/v1/payment"]
browsers = ["Chrome", "Firefox", "Edge", "Safari", "Opera"]
os_types = ["Windows", "macOS", "Linux", "Android", "iOS"]
device_types = ["Desktop", "Mobile", "Tablet"]
error_messages = {
    "500": "Internal Server Error",
    "403": "Forbidden - Access Denied",
    "404": "Page Not Found",
    "503": "Service Unavailable"
}

log_counter = 0


def generate_log():
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    ip = faker.ipv4()
    dt = datetime.datetime.now(local).strftime('%d/%b/%Y:%H:%M:%S')
    tz = datetime.datetime.now(local).strftime('%z')
    session_id = faker.uuid4()
    user_id = random.randint(1000, 9999)

    # FIX: Convert Decimal to Float
    lat, lon = float(faker.latitude()), float(faker.longitude())

    method = random.choice(http_methods)
    uri = random.choice(resources)

    if "/api/v1/" in uri:
        uri += f"/{random.randint(100, 999)}"

    status_code = numpy.random.choice(response_codes, p=[0.85, 0.05, 0.02, 0.04, 0.02, 0.02])
    response_size = int(random.gauss(5000, 50))
    referer = faker.uri()
    referrer_domain = urlparse(referer).netloc
    user_agent = faker.user_agent()
    browser = random.choice(browsers)
    os = random.choice(os_types)
    device_type = random.choice(device_types)
    request_time = round(random.uniform(0.1, 1.5), 3)

    error_message = error_messages.get(str(status_code), "")

    log_entry = {
        "timestamp": timestamp,
        "ip": ip,
        "datetime": f"{dt} {tz}",
        "session_id": session_id,
        "user_id": user_id,
        "lat": lat,  # Now float
        "lon": lon,  # Now float
        "http_method": method,
        "url": uri,
        "status_code": status_code,
        "response_size": response_size,
        "referer": referer,
        "referrer_domain": referrer_domain,
        "user_agent": user_agent,
        "browser": browser,
        "os": os,
        "device_type": device_type,
        "request_time": request_time,
        "error_message": error_message
    }

    return log_entry


def send_log_to_opensearch(log):
    global log_counter
    url = f"{OPENSEARCH_URL}/{INDEX_NAME}/_doc"
    headers = {"Content-Type": "application/json"}

    auth = (USERNAME, PASSWORD) if USERNAME and PASSWORD else None

    try:
        print(f"🔹 Sending log: {log}")

        response = requests.post(url, json=log, headers=headers, auth=auth, verify=False, timeout=10)

        if response.status_code in [200, 201]:
            log_counter += 1
            if log_counter % 10 == 0:
                print(f"✅ {log_counter} logs sent successfully!")

        else:
            print(f"❌ Failed to send log: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"🚨 Connection error: {e}")


while log_lines > 0 or log_lines == float('inf'):
    log = generate_log()
    send_log_to_opensearch(log)

    if args.sleep:
        time.sleep(args.sleep)

    if log_lines > 0:
        log_lines -= 1

print(f"✅ Finished sending {log_counter} logs to OpenSearch!")
