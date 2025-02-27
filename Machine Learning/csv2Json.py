import pandas as pd
import json
import requests
from requests.auth import HTTPBasicAuth

# Load CSV file
csv_file = "C:\\Users\\user\\Downloads\\Ulta_Reviews_processed.csv"  # Change this to your actual CSV file that you want to transform
df = pd.read_csv(csv_file, sep=";")

# Prepare bulk request
bulk_data = ""
index_name = "product_reviews"  # Change this to your OpenSearch index name

for _, row in df.iterrows():
    bulk_data += json.dumps({"index": {"_index": index_name}}) + "\n"
    bulk_data += json.dumps(row.to_dict()) + "\n"  # Convert row to key-value pairs

output_file = "bulk_data.json"  # creates Json to check in case of any errors (only needed for testing or bug fixing)
with open(output_file, "w") as f:
    f.write(bulk_data)

print(f"Bulk data has been written to {output_file}") #user info

# Authentication
auth = HTTPBasicAuth("admin", "PASSWORD")  # Use your OpenSearch admin credentials

# OpenSearch endpoint
opensearch_url = "https://localhost:9200/_bulk"  #if needed change to correct port / URL

# Send bulk request
headers = {"Content-Type": "application/x-ndjson"}
response = requests.post(opensearch_url, data=bulk_data, headers=headers, auth=auth, verify=False)

# Print response
print(response.json())

