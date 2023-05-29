# Shipping Service

[![forthebadge](https://forthebadge.com/images/badges/built-by-codebabes.svg)](https://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

![image](images/cargo.jpg)

*Link to the test task [link](ihttps://faint-adasaurus-4bc.notion.site/web-Python-Middle-c1467cf373c24f0cafb8bfe0fe77cc79).*

# Table of contents

- [Getting Started](#getting-started)

# Getting Started

[(Back to top)](#table-of-contents)

1. Install Git on your machine.  And clone the repository to your machine:
    ```sh
    git clone git@github.com:Batyrhan21/shipping-service.git
    cd shipping-service/
    ```

2. Install Docker and Docker-compose. Have a look at the [Tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)


3. Copy the .envExample file and rename it to .env:
    ```sh
    cp .envExample .env
    ``` 

4. Open the .env file in a text editor and provide the following configuration values:
    ```bash
    SECRET_KEY=
    DEBUG=
    ALLOWED_HOSTS=
    PRODUCTION=
    CORS_ALLOWED_ORIGINS=
    FILE_UPLOAD_MAX_MEMORY_SIZE=
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=
    ```

5. Start the services using shell script:

    *This command will pull the necessary Docker images, create and start the containers defined in the docker-compose.yml and dev/docker-compose-dev.yml file.*

    ```sh
    cd entrypoints/
    ./local_start.sh
    ``` 

    *Wait for the services to start and become healthy. You can monitor the status of the services using the following command:*

    ```sh
    docker-compose ps
    ``` 

6. Ensure that all services, including postgres, back, and redis, are in a healthy state.