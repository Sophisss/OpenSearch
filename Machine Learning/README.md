CSV to Json needed because Data set in CSV format
got a sample data https://www.kaggle.com/datasets/winston56/johnson-johnson-ogx-product-reviews
took only reveiews from 2019 onwards that were not empty => 2213 entries


# 🧠 OpenSearch Product Review Agent

This project demonstrates how to build an intelligent agent using **OpenSearch**, **Hugging Face embeddings**, and **Gemini** to provide natural language answers based on product reviews.

---

## 📦 Overview

- **Dataset**: Product reviews from [Kaggle](https://www.kaggle.com/) reduced to 2,000 entries.
- **Goal**: Enable users to ask questions about products and get contextual, smart answers using vector search + LLM.
- **Tech Stack**:
  - OpenSearch (ML Commons, k-NN, Agent Framework)
  - Hugging Face Sentence Transformers
  - Gemini API (via OpenSearch connector)
  - Python (for data transformation and bulk upload)

---

## 📁 Project Structure

```
📂 project-root/
├── data/
│   └── product_reviews_cleaned.csv   # Cleaned CSV: product + review columns only
├── scripts/
│   └── upload_to_opensearch.py       # Python script for bulk upload
└── README.md                         # This file
```

---

## ⚙️ Step-by-Step Setup

### 1. Prepare the Data
- Download product reviews dataset from Kaggle.
- Clean and reduce to ~2k entries.
- Keep only two columns: `product`, `review`.

### 2. Enable ML Commons + Agent Framework

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

✅ *This enables the use of ML models and agents even without dedicated ML nodes.*

### 3. Register the Hugging Face Embedding Model

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

### 4. Deploy and Test the Model

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

### 5. Create Ingest Pipeline for Text Embeddings

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

### 6. Create k-NN Index with Vector Fields

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
