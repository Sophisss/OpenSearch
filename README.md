# OpenSearch
This project contains the OpenSearch configuration using Docker Compose, along with the documentation that will accompany the project. 

## What is OpenSearch?
OpenSearch is an open-source search and analytics suite designed to provide a scalable and high-performance solution for managing and querying large volumes of data. It is a fork of Elasticsearch and Kibana, developed by Amazon Web Services (AWS) and maintained by the community.

### Key Features:
- **Full-text Search**: Ability to perform advanced search queries on large volumes of data.
- **Scalability**: OpenSearch is designed to scale horizontally, enabling the management of huge amounts of data.
- **Aggregations**: Allows performing advanced data analysis through aggregations and statistics.
- **Kibana Web Interface**: Provides a web interface for interactive visualization and analysis of data.

## Running OpenSearch with Docker Compose
To run OpenSearch on your local environment, you can use Docker and Docker Compose. Below are the steps to configure and start OpenSearch using the `docker-compose.yml` file provided in this repository.

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Instructions
1. **Download the repository files**:
Download or copy the `docker-compose.yml` file from this repository to your local system. You can place them in any folder where you'd like to run OpenSearch.

2. **Check Docker Compose configuration**:  
   Ensure that the `docker-compose.yml` file is properly configured for your environment. You can customize settings like network ports or memory if necessary.

   **Note**:  
   Fresh installs of OpenSearch 2.12 or later require you to define an admin password for `opensearch-node1` and `opensearch-node2` when configuring the security demo. You must set the `OPENSEARCH_INITIAL_ADMIN_PASSWORD` environment variable for these services.

   Example configuration in `docker-compose.yml`:

   ```yaml
   services:
     opensearch-node1:
       environment:
         - OPENSEARCH_INITIAL_ADMIN_PASSWORD=your_password_here

     opensearch-node2:
       environment:
         - OPENSEARCH_INITIAL_ADMIN_PASSWORD=your_password_here
   ```
   Ensure that the password is the same across both nodes and meets OpenSearch's password requirements. For detailed guidance on setting up the password and the requirements, consult the [official guide on demo configuration](https://opensearch.org/docs/latest/security/configuration/demo-configuration/).
   
4. **Start OpenSearch**:
Once you've downloaded the necessary files, navigate to the folder containing `docker-compose.yml` and run the following command to start OpenSearch:

    ```bash
    docker-compose up
    ```
    This will download the necessary Docker images and start the OpenSearch and OpenSearch Dashboards containers (the web interface for managing OpenSearch).

5. **Access OpenSearch Dashboards**:
Once the containers are up and running, you can access OpenSearch Dashboards via your browser at [http://localhost:5601](http://localhost:5601) and log in with the default username `admin` and the password you set in the `docker-compose.yml` file (e.g., `<your-password>`).

6. **Stop the containers**:
When you're done, you can stop the containers with the following command:

    ```bash
    docker-compose down
    ```

    Alternatively, you can stop the containers by pressing `Ctrl + C` in the terminal where you ran `docker-compose up`. This will stop the containers, but     they will remain in a stopped state. To remove them entirely, you should run `docker-compose down`.

## Official OpenSearch Documentation
For more detailed instructions, official downloads, and configuration options, please refer to the [OpenSearch official documentation](https://opensearch.org/downloads.html).

## Documentation
The project report, including further details on installation, configuration, and analysis of OpenSearch, will be available in this repository.
