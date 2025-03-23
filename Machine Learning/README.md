# 🧠 OpenSearch Product Review Agent

This example demonstrates how to build an  agent using **OpenSearch** ML/AI functionalities, **Hugging Face embeddings**, and **Gemini** to provide natural language answers based on product reviews and is one application of the AI/ML features in OpenSearch.

---

## 📦 Overview

- **Dataset**: Product reviews from [Kaggle](https://www.kaggle.com/datasets/winston56/johnson-johnson-ogx-product-reviews) reduced only reveiews from 2019 onwards that were not empty => 2213 entries.
- **Goal**: Enable users to ask questions about products and get contextual, smart answers using vector search + LLM.
- **Tech Stack**:
  - OpenSearch (ML Commons, k-NN, Agent Framework)
  - Hugging Face Sentence Transformers
  - Gemini API (via OpenSearch connector)
  - Python (for csv data transformation and bulk upload)

---
## 🐳 Docker Setup (for Local Development)

To quickly spin up OpenSearch with required nodes and dashboards, use the [`docker-compose.yml`](/Machine%20Learning/docker-compose.yml) setup found in this repo. Main difference to the previously used yaml-file is the addition of a Machine learning dedicated node, as shown below:

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

## 🗃️ Prepare the Data
- Download product reviews dataset from Kaggle.
- Clean and reduce to only 2019 onword entries.
- Keep only two columns: `product`, `review`
- You find the used cleaned up data [.csv-file here](/Machine%20Learning/Ulta_Reviews_processed.csv)
- The data needs to be pushed via the [Python script](/Machine%20Learning/csv2Json.py) into the index in OpenSearch (see step 6. below)

---

## ⚙️ Step-by-Step Setup in OpenSearch

You will find in [ML_ProductAgent_OPQuery.txt](Machine%20Learning/ML_ProductAgent_OPQuery.txt), a commented file with all commands needed to be exceuted in the DEVTools Commandline in OpenSearch Dashboard: upper left menu Navigation => scroll down to "Management" => click on Dev Tools. 


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

✅ *This pipeline will run on document ingestion and create vector embeddings and will store the vectors in the fields with "..._embedding".*

### 5. Create Index with Vector Fields

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

✅ *Configures the index for vector search and attaches the ingest pipeline so it is being run whenever new data arise.*

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
    "description": "The connector to public Gemini model free sercice",
    "version": 1,
    "protocol": "http",
    "parameters": {
        "endpoint": "generativelanguage.googleapis.com",
        "model": "gemini-1.5-flash",
        "APIkey": "YOURGEMINIAPIKEY"
    },
    "credential": {
        "dummy": "dummy"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://${parameters.endpoint}/v1beta/models/${parameters.model}:generateContent?key=${parameters.APIkey}",
            "headers": {
                "Content-Type": "application/json"
            },
            "request_body": "{ \"contents\": [{ \"parts\": [{ \"text\": \"${parameters.prompt}\" }] }] }"
        }
    ]
}
```

✅ *Dummy credentials are required even if unused, as required by OpenSearch but not from Gemini. Note connector ID.*
ℹ️ *the connection offers an action that is called "predict" which takes the parameters from the user input of the action and does prompt it to Gemini*

### 9. Register & Deploy Gemini Model

```json
POST /_plugins/_ml/models/_register
{
    "name": "Gemini Flash Model 1.5",
    "function_name": "remote",
    "description": "Gemini Flash 1.5v Model",
    "connector_id": "CONNECTORID"
}
```
ℹ️ *registers the connector just created in a model (write down Model ID (referred later as YOURMODELIDGEMINI)*

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
    "name": "Product Review Agent 2",
    "type": "conversational_flow",
    "description": "This is a demo agent for giving information about products regarding reviews",
    "app_type": "rag",
    "memory": {
        "type": "conversation_index"
    },
    "tools": [
        {
            "type": "VectorDBTool",
            "name": "product_knowledge_base",
            "parameters": {
                "model_id": "YOURMODELID",
                "index": "product_reviews",
                "embedding_field": "product_embedding",
                "source_field": [
                    "product"
                ],
                "input": "${parameters.question}"
            }
        },
                {
            "type": "VectorDBTool",
            "name": "review_knowledge_base",
            "parameters": {
                "model_id": "YOURMODELID",
                "index": "product_reviews",
                "embedding_field": "review_embedding",
                "source_field": [
                    "review"
                ],
                "input": "${parameters.question}"
            }
        },
        {
            "type": "MLModelTool",
            "name": "bedrock_claude_model",
            "description": "A general tool to answer any question",
            "parameters": {
                "model_id": "MODELIDFROMGEMINIMODEL",
                "prompt": "\n\nHuman:You are a professional sentiment analysist and you can answer questions regarding reviews of products. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't have enough context, you will ask Human to provide more information. If you don't know the answer, just say don't know. \n\n Context:\n${parameters.product_knowledge_base.output}\n\n${parameters.review_knowledge_base.output}\n\nHuman:${parameters.question}\n\nAssistant:"
            }
        }
    ]
}
```

✅ *Creates an Agent (write down AgentID), including tools for vector search and LLM prompting.*

### 11. Interact with the Agent

```json
POST /_plugins/_ml/agents/YOURAGENTID/_execute
{
  "parameters": {
    "question": "How would you summarize the reviews for Morocco Extra Penetrating Oil?"
  }
}
```

### 🧪 Example Output

> *The reviews for  Morocco Extra Penetrating Oil are overwhelmingly positive. One reviewer raves about its effectiveness in preventing split ends and heat damage, praising its pleasant scent and efficiency (a little goes a long way). Another reviewer reports that their daughter loves the product and particularly enjoys the smell. Both reviews highlight the positive sensory experience (smell)*

---

## 💡 Future Enhancements

- Add web UI, curently we can address the Agent with a REST call or a Dev Tools command, but it would be nice to have a built in chatbot for such request for OpenSearch dashboard users.

---

## 📚 References

- [OpenSearch ML Commons](https://opensearch.org/docs/latest/ml-commons/)
- [Gemini API](https://ai.google.dev/)
- [Chat GPT](https://chatgpt.com/)
