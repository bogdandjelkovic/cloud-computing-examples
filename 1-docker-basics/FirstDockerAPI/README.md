# Example 1: Docker basics

Commands to run `FirstDockerAPI`:

```bash
docker build -t first-docker-api .

docker run -p 8080:8080 --name first-docker-api first-docker-api
```

Test route:
```http
http://localhost:8080/weatherforecast
```