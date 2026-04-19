# Vector Database Course: Docker Environment

This folder contains the environment configuration needed to run the Day 1 and Day 2 Vector Database engineering labs.

We use **Docker** to ensure that your environment completely mimics a production server stack and guarantees everyone the exact right version of Redis Graph architectures.

## Pre-requisites
- Have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

## Option 1: Quick Command (No config needed)
To deploy the database right now via CLI without `docker-compose`:
```bash
docker run -d --name redis-vector-db -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

## Option 2: Docker Compose (Recommended)
We have provided a `docker-compose.yml` in this folder. It scales perfectly for our labs.
1. Open your terminal in this directory.
2. Run the command: `docker-compose up -d`
3. Wait for the containers to spin up.

## Verification
You can verify the database is active by opening **RedisInsight**, the visual Database Admin UI.
Navigate to your web browser and open:
[http://localhost:8001](http://localhost:8001)
