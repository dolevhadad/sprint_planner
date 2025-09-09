# Dockerfiles README
 [Back to main project README](README.md)

This directory contains Dockerfiles used to build and run the sprint planning application.

## Files


## Usage

### Build Local Image
```

### Build Production Image
```
docker build -f Dockerfile.prod -t sprint-planning-prod .
```

### Run Container
```
docker run -p 8000:8000 sprint-planning
```

### Using Docker Compose
Docker Compose allows you to manage multi-container setups, environment variables, and networking with a single configuration file.

#### Start the application with Docker Compose
```
docker-compose up --build
```
This command builds the images (if needed) and starts all services defined in `docker-compose.yml`.

#### Stop the application
```
docker-compose down
```
This stops and removes all containers defined in the compose file.

#### Notes
- Docker Compose is useful for local development and testing, especially if you add databases or other services.
## Notes
