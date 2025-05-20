# 🛡️ IAM Architecture with Flask, Keycloak, and Docker Compose

This project demonstrates a secure **Identity and Access Management (IAM)** architecture using:

- 🔐 [Keycloak](https://www.keycloak.org/) as the Identity Provider
- 🐍 Flask as a protected Python API
- 🐳 Docker Compose for container orchestration

---

## 📐 Architecture Diagram

```mermaid
flowchart TD
    U[User] --> C["Browser / cURL"]
    C --> K["Keycloak IAM Server"]
    C --> F["Flask App - Protected API"]
    F --> K
```

---

## ⚙️ Features

- 🔒 Token-based access control via Keycloak (OpenID Connect)
- ✅ Public and protected API routes in Flask
- 🧪 Test automation using Makefile
- 📈 Docker security checks with Docker Bench for Security
- 🟢 Health checks for both containers
- 🧱 Hardened container config using `read_only`, `cap_drop`, `security_opt`, and memory/CPU/PID limits

---

## 📁 Project Structure

```
.
├── flaskapp/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── .env
├── docker-compose.yml
├── keycloak-setup.sh
├── Makefile
├── README.md
├── realm-config.json
└── test-flask.sh
```

---

## 📁 Key Components Reviewed

| Component | Evaluation |
|----------|------------|
| `docker-compose.yml` | ✅ Hardened containers (memory, pids, CPU, capabilities), health checks |
| `Makefile` | ✅ Streamlined automation with `reset`, `check`, `setup-keycloak` targets |
| `keycloak-setup.sh` | ✅ Creates realm, client, user with correct attributes and secure password setup |
| `test-flask.sh` | ✅ Validates JWT auth against Flask endpoints using curl and bearer tokens |
| `flaskapp/app.py` | ✅ Verifies token using python-jose, with structured error logging |
| `Dockerfile` | ✅ Non-root user, minimal Alpine base, healthcheck added |
| `.env` | ✅ Used consistently across scripts and compose |
| `README.md` | ✅ Includes usage, architecture, and security hardening notes |
| `realm-config.json` | ✅ Optional backup or export of realm settings |
| Security | ✅ Applied Bandit checks, Docker Bench findings addressed where feasible |

---

## 🚀 Quick Start

### 🔧 Prerequisites

- Docker + Docker Compose
- Make
- `jq` (for parsing tokens)
- Git Bash or a Unix-like terminal on Windows

---

### 🔨 Build and Run

```bash
make reset           # Cleans, builds, and starts the environment
make setup-keycloak  # Creates Keycloak realm, client, and test user
```

---

### 🔐 API Endpoints

| Endpoint        | Auth Required | Description              |
|-----------------|---------------|--------------------------|
| `/public`       | ❌ No          | Public endpoint          |
| `/protected`    | ✅ Yes         | Requires Bearer token    |
| `/health`       | ❌ No          | Used by Docker healthcheck |

---

## 🧪 Testing Access

```bash
make test-flask
```

This will:

- Call `/public` (200 OK)
- Call `/protected` without token (401 Unauthorized)
- Call `/protected` with a valid token (200 OK)

---

## 🔧 Keycloak Default Settings

| Setting       | Value            |
|---------------|------------------|
| Realm         | `demo-realm`     |
| Client ID     | `flask-client`   |
| Client Secret | `secret`         |
| Username      | `testuser`       |
| Password      | `testpass`       |

You can log in to the [Keycloak Admin Console](http://localhost:8080/admin/) using:

- **Username:** `admin`
- **Password:** `admin`

---

## 🔒 Security Hardening Notes

The IAM environment is hardened with multiple Docker security measures for both the Flask and Keycloak services.

### 🧱 Container Runtime Security

| Control                   | `keycloak`                          | `flaskapp`                                 | Purpose                                                                 |
|---------------------------|-------------------------------------|---------------------------------------------|-------------------------------------------------------------------------|
| `read_only`               | ❌ Not set                          | ✅ `read_only: true`                        | Prevents write access to container filesystem                          |
| `security_opt`            | `label=type:container_t`           | `label=type:container_t`, `no-new-privileges:true` | SELinux label + blocks privilege escalation                            |
| `cap_drop`                | ❌ Not set                          | ✅ `cap_drop: ALL`                          | Drops all Linux capabilities by default                                |
| `cap_add`                 | ❌ Not set                          | ✅ `NET_RAW`                                | Needed for `curl` in Alpine healthcheck                                |
| `restart` policy          | ✅ `on-failure:5`                   | ✅ `on-failure:5`                           | Resilience with limited retry attempts                                 |
| `healthcheck`             | ✅ Configured (realm check)         | ✅ Configured (`/health` endpoint)          | Ensures services are monitored and restarted if unhealthy              |

---

### 🚦 Resource Limits

| Resource | Limit     | Applies To   | Purpose                                         |
|----------|-----------|--------------|-------------------------------------------------|
| Memory   | `512M` (Keycloak), `200M` (Flask) | Both | Prevents excessive memory usage              |
| PIDs     | `300` (Keycloak), `100` (Flask)   | Both | Limits thread/process spawning               |
| CPU      | `cpu_quota: 100000` (Keycloak), `50000` (Flask) | Both | Explicitly limits CPU usage (1.0 & 0.5 cores) |

---

### 💾 Volume Isolation

| Volume         | Purpose                          |
|----------------|----------------------------------|
| `keycloak-data`| Stores realm config and user data |
| _(none)_       | Flask app is stateless and readonly |

---

## 📦 Useful Makefile Targets

```bash
make build           # Docker Compose build
make start           # Start containers
make stop            # Stop containers
make logs            # View logs
make setup-keycloak  # Configure Keycloak realm, client, user
make test-flask      # Run test to validate protected access
make clean           # System prune
make reset           # Full clean, build, and start
```

---

## ✅ Suggestions (Optional Improvements)

- Consider mounting secrets from `.env` using Docker secrets in production
- Enforce HTTPS (TLS) with a reverse proxy (e.g., Nginx, Caddy)
- Add AppArmor or Seccomp profiles for full compliance
- Use `python-dotenv` in `app.py` for `.env` loading in non-Docker runs

---

## 🔐 OAuth 2.0 and OIDC Flows Implemented

This project uses the **Resource Owner Password Credentials Grant** flow from OAuth 2.0, enhanced with OpenID Connect (OIDC) for identity support.

### Flow Summary:
1. **User** authenticates by sending credentials to Keycloak's `/token` endpoint.
2. **Keycloak** verifies the credentials and returns:
   - `access_token` (OAuth 2.0)
   - `id_token` (OIDC)
3. **Client (Flask App)** sends `access_token` in the `Authorization: Bearer` header.
4. **Flask app** fetches Keycloak's public keys (JWKS) and verifies the JWT.
5. If valid, user is allowed access to protected resources.

**OIDC Claim Use:** The JWT includes OIDC claims such as `email_verified`, `preferred_username`, `given_name`, and `family_name`, which help establish trusted identity.

---

## 🔐 Security Analysis (STRIDE)

| STRIDE Threat | Risk Description | Mitigation Applied |
|---------------|------------------|---------------------|
| **S**poofing         | Forged tokens to impersonate users | JWT signature validation with RS256 using Keycloak’s public key |
| **T**ampering        | Token or API request manipulation | JWT integrity ensured with cryptographic signature |
| **R**epudiation      | User denial of actions | JWT contains traceable `sub`, `iat`, and session ID |
| **I**nformation Disclosure | Exposure of sensitive data or credentials | Minimal API exposure; secrets stored in `.env`, not in image |
| **D**enial of Service | Exhaustion of system resources | Resource constraints via `cpu_quota`, memory, and `pids` limits |
| **E**levation of Privilege | Unauthorized access to protected routes | Token claims must match realm roles; no admin access granted |

---

## 🧠 Reflection on the Okta Case Study

### Incident Summary:
Okta experienced breaches due to:
- Improper access controls for third-party contractors
- Session token hijacking
- Excessive role privileges and poor telemetry

### Impacts on This Project:

| Okta Lesson | Mitigation in Your Project |
|-------------|----------------------------|
| Token hijacking | Tokens expire and must be freshly issued |
| Overprivileged accounts | Only minimal roles and test user with scoped client access |
| Insecure credentials | All secrets isolated via `.env` and never hard-coded |
| No central audit | JWT logs printed on invalid token access, supporting future observability |

This reflection shaped the design by reinforcing the principles of **least privilege**, **secure secret handling**, and **token validation**.

---

## ✅ Summary

This IAM architecture demonstrates:
- A secure OAuth 2.0 + OIDC implementation with Keycloak and Flask
- Container hardening with Docker resource limits, `cap_drop`, and health checks
- Threat modeling with STRIDE and corresponding mitigations
- Learned practices from real-world identity breaches (Okta)

It represents a strong example of identity and access management architecture in a containerized environment.

---

## 📘 References

- [Keycloak Documentation](https://www.keycloak.org/docs/latest/)
- [Docker Bench for Security](https://github.com/docker/docker-bench-security)
- [Flask](https://flask.palletsprojects.com/)
- [Python-JOSE](https://python-jose.readthedocs.io/en/latest/)

---

## 🧑‍💻 Author

**Timothy Brennan**  
For educational use in IAM and container security labs.

---