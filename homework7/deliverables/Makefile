PYTHON_IMAGE=python:3.13.3-alpine

check:
	@echo "Running code analysis with Bandit..."
	docker run --rm -v $(PWD):/app $(PYTHON_IMAGE) sh -c "pip install bandit && bandit -r /app"
	@echo "Running dependency check with pip-audit..."
	docker run --rm -v $(PWD):/app $(PYTHON_IMAGE) sh -c "pip install pip-audit && pip-audit -r /app/requirements.txt"

# Host security check
host-security:
	@echo "Running Docker Bench for Security..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security

# Build Docker image after security checks
dbuild: check
	docker build -t mywebapp .

# Run the container
run:
	docker run -p 6000:5000 mywebapp

# High-level image recommendations (best practices, outdated base images, etc.)
scan: dbuild
	docker scout recommendations

# Security vulnerability scan (CVEs in OS and app layers)
scan-cves:
	docker scout cves mywebapp:latest --only-severity high,critical

# Docker Compose commands
build:
	docker compose build

start:
	docker compose up -d

stop:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker system prune -f

restart: stop start
