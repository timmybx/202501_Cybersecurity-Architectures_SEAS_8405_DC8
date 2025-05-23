PYTHON_IMAGE=python:3.13.3-alpine
APP_NAME=flaskapp

check:
	@echo "Running Bandit (Python code analysis)..."
	docker run --rm -v $(PWD):/app $(PYTHON_IMAGE) sh -c "pip install bandit && bandit -r /app/$(APP_NAME)"
	@echo "Running pip-audit (dependency audit)..."
	docker run --rm -v $(PWD):/app $(PYTHON_IMAGE) sh -c "pip install pip-audit && pip-audit -r /app/$(APP_NAME)/requirements.txt"

host-security:
	@echo "Running Docker Bench for Security..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security

scan: build
	docker scout recommendations

scan-cves:
	docker scout cves mywebapp:latest --only-severity high,critical

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

reset: clean check host-security stop build start
	@echo "Waiting for Keycloak endpoint to respond..."
	@timeout 300 bash -c 'until curl --silent --fail http://localhost:8080/realms/master > /dev/null; do echo "Still waiting for Keycloak..."; sleep 5; done'
	@echo "Environment is ready!"

setup-keycloak:
	./keycloak-setup.sh

test-flask:
	./test-flask.sh
