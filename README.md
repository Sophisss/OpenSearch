# OpenSearch
This project contains the OpenSearch configuration using Docker Compose, along with detailed documentation to help you set up and explore OpenSearch efficiently.

## **What is OpenSearch?**  
OpenSearch is an **open-source search and analytics suite** designed to provide scalable, high-performance data management. It enables businesses to **index, search, and analyze** vast amounts of data with features such as full-text search, aggregations and interactive dashboards. 

It is a fork of Elasticsearch and Kibana, originally developed by Amazon Web Services (AWS) and maintained by the OpenSearch community.

### **Key Features:** 
- 🔍 **Advanced Search Capabilities**: Perform complex full-text searches on large datasets.
- 📈 **Scalability**: OpenSearch is designed to scale horizontally, enabling the management of huge amounts of data.
- 📊 **Aggregations & Analytics**: Execute statistical queries and derive insights from structured and unstructured data.
- 📉 **Interactive Dashboards**: OpenSearch Dashboards provide a web-based interface for data visualization and monitoring.
- 🤖 **AI/ML Integrations**: Supports AI-driven features like anomaly detection and predictive analytics.

## **Project Overview and Objectives** 
This project aims to explore and evaluate OpenSearch with a focus on its core functionalities, integrations and use cases. The objectives include:
- 🔍 **Observability Analysis**: Study how OpenSearch integrates with observability tools and its compatibility with OpenTelemetry.
- 📊 **Feature Exploration**: Investigate OpenSearch's capabilities in search, analytics, and visualization.
- 🤖 **AI/ML Support**: Evaluate OpenSearch's AI/ML features, such as anomaly detection.
- 🎯 **Hands-on Deployment**: Set up OpenSearch locally using Docker Compose for hands-on experimentation.
  
## **How to Set Up OpenSearch Locally with Docker Compose** 
To start using OpenSearch, it is recommended to deploy it in a local or cloud-based environment. One of the most efficient ways to install OpenSearch is via **Docker Compose**, which simplifies deployment by managing OpenSearch and its dependencies in isolated containers.

Follow these steps to setup OpenSearch using Docker Compose:

### **Prerequisites**  
Ensure you have the following tools installed on your system:  
1. [Docker](https://www.docker.com/get-started) 🐳 - Containerization platform required for deployment.
   
   - To verify installation, run:
     
     ```bash
       docker --version
       ```
2. [Docker Compose](https://docs.docker.com/compose/) 🛠️ - Tool for managing multi-container applications.

   - To verify installation, run:
     
     ```bash
       docker-compose --version
       ```

### **Setup Instructions** 

1. **Clone or Download this Repository** 📂:  
   Download or clone the repository containing the `docker-compose.yml` file to your local system. You can choose the directory where you'd like to run OpenSearch.

2. **Understand the Configuration** 💡:  

   The `docker-compose.yml` file typically defines a minimal OpenSearch cluster with two nodes: 
     - `opensearch-node1`: Handles indexing and search operations.  
     - `opensearch-node2`: Works alongside node1 to provide redundancy and scalability.  
   
   This setup ensures: 
   - **Fault tolerance**: If one node fails, the other continues operations.
   - **Scalability**: Workloads are distributed across multiple nodes, improving performance.
   - **Advanced search capabilities**: Supports full-text search, log analysis, and machine learning-based anomaly detection.

3. **Customize Configuration** ⚙️:  
   Open the `docker-compose.yml` file and configure it according to your environment. For example, you can change port mappings or memory settings based on your system's resources.

   > ⚠️ **Security Note:**  
   > For OpenSearch 2.12 or later, you must define an admin password for both `opensearch-node1` and `opensearch-node2` when configuring the security demo. Set the `OPENSEARCH_INITIAL_ADMIN_PASSWORD` environment variable in `docker-compose.yml`:
   > 
   > **Example configuration:**
   > 
   > ```yaml
   > services:
   >   opensearch-node1:
   >     environment:
   >       - OPENSEARCH_INITIAL_ADMIN_PASSWORD=your_password_here
   > 
   >   opensearch-node2:
   >     environment:
   >       - OPENSEARCH_INITIAL_ADMIN_PASSWORD=your_password_here
   > ```
   >
   > Ensure that the password is the same across both nodes and meets OpenSearch's password requirements. For detailed guidance on setting up the password and the requirements, consult the [official guide on demo configuration](https://opensearch.org/docs/latest/security/configuration/demo-configuration/).
   
   
4. **Start OpenSearch** ▶️:  
Once the configuration is complete, navigate to the directory containing `docker-compose.yml` and run the following command to start the cluster in detached mode:

    ```bash
    docker-compose up -d
    ```
    This will download the necessary Docker images and launch OpenSearch along with OpenSearch Dashboards.
   
    By default: 
      - OpenSearch is accessible at http://localhost:9200
      - OpenSearch Dashboards is accessible at http://localhost:5601

5. **Verify OpenSearch is Running** ✅:  
   To check if OpenSearch is active, visit http://localhost:9200 in a browser or run:
   ```bash
    curl -X GET "http://localhost:9200" 
    ```
   A successful response should return JSON output similar to:
   ```json
    {
    "name": "opensearch-node1",
    "cluster_name": "opensearch-cluster",
    "cluster_uuid": "8qHNNTCSRlWke8As-EOl8w",
    "version": {
        "distribution": "opensearch",
        "number": "2.18.0",
        "build_type": "tar",
        "build_hash": "99a9a81da366173b0c2b963b26ea92e15ef34547",
        "build_date": "2024-10-31T19:08:04.231254959Z",
        "build_snapshot": false,
        "lucene_version": "9.12.0",
        "minimum_wire_compatibility_version": "7.10.0",
        "minimum_index_compatibility_version": "7.0.0"
    },
    "tagline": "The OpenSearch Project: https://opensearch.org/"
   }
    ```
   Additionally, to confirm the containers are running properly, check your Docker container list. You should see both OpenSearch nodes (opensearch-node1 and opensearch-node2) as well as the OpenSearch Dashboards container, confirming that the entire OpenSearch cluster is operational. 

6. **Exploring OpenSearch Dashboard** 🌐:   
   After successfully launching OpenSearch, you can access the OpenSearch Dashboard, a graphical interface that allows you to interact with indexed data, create visualizations, and monitor system performance.

   To open OpenSearch Dashboard, navigate to http://localhost:5601 and log in with the default username `admin` and the password you set in the `docker-compose.yml` file (e.g., `<your-password>`).

7. **Stopping the OpenSearch Cluster** ⏹️:  
When you're done, you can stop the containers with the following command:

    ```bash
    docker-compose down
    ```
   
   This command will shut down and remove all containers, networks, and volumes associated with the OpenSearch deployment.

    Alternatively, you can stop the containers by pressing `Ctrl + C` in the terminal where you ran `docker-compose up`. This will stop the containers, but they will remain in a stopped state. To remove them entirely, you should run `docker-compose down`.

## **Troubleshooting** 🛠️
If you encounter issues, here are some common solutions:
1. **Ports Already in Use**
   
   If port `9200` (OpenSearch) or `5601` (Dashboards) is occupied, modify `docker-compose.yml`:
   ```yaml
     ports:
       - "9201:9200" # Change the external port
       - "5602:5601"
    ```
   After making changes, restart OpenSearch with:
   ```bash
   docker-compose down && docker-compose up
    ```
2. **Authentication Errors**

   - Ensure that the admin password is set correctly in `docker-compose.yml`.
   - Restart OpenSearch to apply the password change.

3. **Container Not Starting**

   If OpenSearch doesn't start correctly, check the logs for error messages:
   ```bash
   docker-compose logs opensearch-node1
    ```
   If the issue persists, remove existing volumes and restart:
   ```bash
   docker-compose down -v && docker-compose up
    ```

## Official OpenSearch Documentation 📚
For more detailed instructions, official downloads, and configuration options, please refer to the [OpenSearch official documentation](https://opensearch.org/downloads.html).

## Project Report and Additional Documentation 📝
The complete project report, including further details on OpenSearch’s capabilities, configuration, and analysis, will be available in this repository. The documentation will also include additional use cases, performance benchmarks, and guides to help you explore OpenSearch in depth.
