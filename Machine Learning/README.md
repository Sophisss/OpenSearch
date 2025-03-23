# 🧠 OpenSearch Product Review Agent

This example demonstrates how to build an  agent using **OpenSearch**, **Hugging Face embeddings**, and **Gemini** to provide natural language answers based on product reviews and is one application of the AI/ML features in OpenSearch.

---

## 📦 Overview

- **Dataset**: Product reviews from [Kaggle]([https://www.kaggle.com/datasets/winston56/johnson-johnson-ogx-product-reviews]) reduced only reveiews from 2019 onwards that were not empty => 2213 entries.
- **Goal**: Enable users to ask questions about products and get contextual, smart answers using vector search + LLM.
- **Tech Stack**:
  - OpenSearch (ML Commons, k-NN, Agent Framework)
  - Hugging Face Sentence Transformers
  - Gemini API (via OpenSearch connector)
  - Python (for csv data transformation and bulk upload)

---

## 📁 Project Structure

```
📂 project-root/d
├── data/
│   └── product_reviews_cleaned.csv   # Cleaned CSV: product + review columns only
├── scripts/
│   └── upload_to_opensearch.py       # Python script for bulk upload
└── README.md                         # This file
```

---
## 🐳 Docker Setup (for Local Development)

To quickly spin up OpenSearch with required nodes and dashboards, use the `docker-compose.yml` setup found in this repo. Main difference to the previously used yaml-file is the addition of a ML dedicated node. as shown below:

```yaml
  opensearch-ml1:
    image: opensearchproject/opensearch:2
    container_name: opensearch-ml1
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-ml1
      - node.roles=ml
      - discovery.seed_hosts=opensearch-node1,opensearch-node2
      - cluster.initial_cluster_manager_nodes=opensearch-node1,opensearch-node2
      - bootstrap.memory_lock=true
      - OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=your_password_here
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-ml1:/usr/share/opensearch/data
    networks:
      - opensearch-net

volumes:
  opensearch-ml1:
```

> ℹ️ **Note**: Replace `your_password_here` with a secure admin password.

## 🗃️ 1. Prepare the Data
- Download product reviews dataset from Kaggle.
- Clean and reduce to only 2019 onword entries.
- Keep only two columns: `product`, `review`
- You find the used cleaned up data as a file in this project.
- The data needs to be pushed via the [Python script](Machine Learning/csv2Json.py) into the index in OpenSearch (see step 6. below)

## ⚙️ 2. Step-by-Step Setup in OpenSearch

You will find in [ML_ProductAgent_OPQuery.txt](Machine Learning/ML_ProductAgent_OPQuery.txt), a commented file with all commands needed to be exceuted in the DEVTools Commandline in OpenSearch Dashboard: upper left menu Navigation => scroll down to "Management" => click on Dev Tools. 



### 1. Enable ML Commons + Agent Framework

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.only_run_on_ml_node": false,
    "plugins.ml_commons.native_memory_threshold": 100,
    "plugins.ml_commons.agent_framework_enabled": true
  }
}
```

✅ *This enables the use of ML models and agents even without dedicated ML nodes. And also solves a known circuit breaker issue*

### 2. Register the Hugging Face Embedding Model

```json
POST /_plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/all-MiniLM-L12-v2",
  "version": "1.0.1",
  "model_format": "TORCH_SCRIPT"
}
```

✅ *This model will convert text into dense vector embeddings.*

⏺ **Note down the returned `task_id`**, then use it to retrieve the model ID:

```json
GET /_plugins/_ml/tasks/TASKID
```

### 3. Deploy and Test the Model

```json
POST /_plugins/_ml/models/MODELID/_deploy
```

Then test the embedding:

```json
POST /_plugins/_ml/models/MODELID/_predict
{
  "text_docs":[ "I go home!"],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```

✅ *Verifies that text-to-vector transformation works.*

### 4. Create Ingest Pipeline for Text Embeddings

```json
PUT /_ingest/pipeline/product_reviews_data_pipeline
{
  "description": "text embedding pipeline for product review usecase",
  "processors": [
    {
      "text_embedding": {
        "model_id": "YOURMODELID",
        "field_map": {
          "review": "review_embedding"
        }
      }
    },
    {
      "text_embedding": {
        "model_id": "YOURMODELID",
        "field_map": {
          "product": "product_embedding"
        }
      }
    }
  ]
}
```

✅ *This pipeline will run on document ingestion and create vector embeddings.*

### 5. Create k-NN Index with Vector Fields

```json
PUT product_reviews
{
  "mappings": {
    "properties": {
      "product": { "type": "text" },
      "product_embedding": { "type": "knn_vector", "dimension": 384 },
      "review": { "type": "text" },
      "review_embedding": { "type": "knn_vector", "dimension": 384 }
    }
  },
  "settings": {
    "index": {
      "knn.space_type": "cosinesimil",
      "default_pipeline": "product_reviews_data_pipeline",
      "knn": "true"
    }
  }
}
```

✅ *Configures the index for vector search and attaches the ingest pipeline.*

### 6. Push data with [Python script](Machine Learning/csv2Json.py) into index
As data can not directly be imported as csv into OpenSearch, Use the script to tranform into bulk upload JSon and send via REST to OpenSearch. You can check if succesfull under upper left menu Navigation => scroll down to "Management" => click on Index Management => check the produc_review index for entries

### 7. Enable Access Control for External Connectors

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.connector_access_control_enabled": true
  }
}
```

✅ *Required to use external services like Gemini.*

Whitelist Gemini endpoints:

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.trusted_connector_endpoints_regex": [
      "^https://runtime\.sagemaker\..*[a-z0-9-]\.amazonaws\.com/.*$",
      "^https://api\.openai\.com/.*$",
      "^https://generativelanguage\.googleapis\.com/.*$",
      "^https://api\.cohere\.ai/.*$",
      "^https://bedrock-runtime\..*[a-z0-9-]\.amazonaws\.com/.*$"
    ]
  }
}
```

### 8. Create Gemini Connector

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Gemini Chat Connector",
  "description": "The connector to public Gemini model free service",
  ...
}
```

✅ *Dummy credentials are required even if unused. Note connector ID.*

### 9. Register & Deploy Gemini Model

```json
POST /_plugins/_ml/models/_register
```

Deploy it:

```json
POST /_plugins/_ml/models/YOURMODELIDGEMINI/_deploy
```

Test with:

```json
POST /_plugins/_ml/models/YOURMODELIDGEMINI/_predict
{
  "parameters": {
    "prompt": "What is Camerino?"
  }
}
```

### 10. Register the Agent

```json
POST /_plugins/_ml/agents/_register
{
  ...
}
```

✅ *Includes tools for vector search and LLM prompting.*

### 11. Interact with the Agent

```json
POST /_plugins/_ml/agents/YOURAGENTID/_execute
{
  "parameters": {
    "question": "How would you summarize the reviews for Morocco Extra Penetrating Oil?"
  }
}
```

---

## 🧪 Example Output

> *Most users appreciate its nourishing properties, especially for dry or damaged hair. It leaves hair soft, shiny, and frizz-free with a pleasant scent.*

---

## 💡 Future Enhancements

- Add web UI
- Sentiment classification
- Streaming ingestion

---

## 📚 References

- [OpenSearch ML Commons](https://opensearch.org/docs/latest/ml-commons/)
- [Gemini API](https://ai.google.dev/)
- [Hugging Face Sentence Transformers](https://www.sbert.net/)
