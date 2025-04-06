# 📊 OpenSearch Dashboard: HTTP Logs with Geolocation

This project sets up an OpenSearch index and dashboard to visualize HTTP log data enriched with geographic coordinates.

## 🛠️ Setup Instructions

To ingest and visualize geospatial data (from separate `lat` and `lon` fields), follow these steps:

---

### 1. Create an Ingest Pipeline

This pipeline combines `lat` and `lon` fields into a `location` field (type `geo_point`).

```json
PUT _ingest/pipeline/add-geopoint
{
  "description": "Create location geo_point from separate lat/lon",
  "processors": [
    {
      "set": {
        "field": "location",
        "value": "{{lat}},{{lon}}"
      }
    }
  ]
}
