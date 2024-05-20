# Bislang Application

This README provides detailed instructions on how to install and run the Bislang application, a fun translation game for learning Bisaya, inside a Docker container using `docker-compose`.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Docker
- Docker Compose

You can check if Docker and Docker Compose are installed by running:
```bash
docker --version
docker-compose --version
```

## Installation

### Clone the repository

If you have a Git repository, clone it. Otherwise, ensure you have your Bislang project ready.

```bash
git clone https://github.com/HHuuxx/bislang-backend.git
cd bislang
```

### Build the Docker images

Navigate to the directory containing your docker-compose.yml file and run the following command to build your Docker images.

```bash
docker-compose build
```


## Running The Application
### Start the containers

Use docker-compose up to start your Docker containers. The -d flag is used to run the containers in detached mode.

```bash
docker-compose up -d
```

### Apply migrations

After your containers are running, you need to apply the Django migrations. Find the name or ID of your Bislang application's container using:
```bash
docker ps
```

Then, run the migrations by executing:

```bash
docker exec -it <container_name_or_id> python manage.py migrate
```

## Usage

Once your application is running, you can access it at http://localhost:8000, or another port if you configured it differently in your docker-compose.yml.


## Managing The Application

### View logs

To check the logs of your Bislang application, use:
```bash
docker-compose logs
```
### Stop the application

To stop your Docker containers, run:

```bash
docker-compose down
```

## Additional Commands

### Creating a Django superuser

To create a Django superuser, run:

```bash
docker exec -it <container_name_or_id> python manage.py createsuperuser
```