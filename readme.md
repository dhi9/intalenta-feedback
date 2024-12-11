## Requirements
- Docker
- Docker Compose

## Project Structure

- **Django**: Web application
- **Celery**: Asynchronous task queue for background processing
- **Redis**: Broker for Celery
- **PostgreSQL**: Database for storing data



## Setup Instructions

### 1. Clone the Repository
Clone the repository 
```
git clone git@github.com:dhi9/intalenta-feedback.git
cd intalenta-feedback
```

### 2. Build and Start Containers
Run the following command to build and start the Docker containers:
```
docker-compose up --build
```

### 3. Access the Services
Once the containers are up and running, you can access the services:
```
http://localhost:8000 
```

### 4. Check Logs
To check logs for any issues or information about the services:
```
Django logs: docker-compose logs backend
Celery logs: docker-compose logs celery
```


### Others Command
Run Migration inside container `docker-compose exec backend bash`
```
python manage.py makemigrations
python manage.py migrate
```
To stop the running containers:
```
docker-compose down
```
To rebuild the images after making changes to the Dockerfile or docker-compose.yml:
```
docker-compose up --build
```
To view the status of all containers:
```
docker-compose ps
```