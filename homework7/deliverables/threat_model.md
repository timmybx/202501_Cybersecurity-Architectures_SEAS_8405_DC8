# Threat Model: Secure Containerized Python Web App

## 1. Overview
This document outlines the threat modeling exercise performed on the updated containerized Python application, following STRIDE and MITRE ATT&CK methodologies. 

---

## 2. STRIDE Analysis

| Threat Category        | Example                                  | Impact                     | Mitigation                            |
|------------------------|------------------------------------------|----------------------------|----------------------------------------|
| Spoofing               | Hardcoded `APP_PASSWORD` with no auth    | Unauthorized access        | Move to `.env`; use token auth        |
| Tampering              | Unsafe IP input to `/ping`               | Command injection          | Use `ipaddress` validation + `subprocess` safety |
| Repudiation            | No app or container logging              | No audit trail             | Add structured logging (`/logs`, Compose) |
| Information Disclosure | Exposed container port on 0.0.0.0        | Internal data exposure     | Bind to `127.0.0.1`; use Compose isolation |
| Denial of Service      | Unrestricted `ping`, `eval()`            | Resource exhaustion        | Add limits, validate inputs, remove `eval` |
| Elevation of Privilege | Container runs as root by default        | Full system compromise     | Add `USER appuser`, `cap_drop: ALL`   |

---

## 3. MITRE ATT&CK Mapping (Containers)

| Tactic             | Technique ID | Technique Name                    | Application Relevance                    |
|--------------------|--------------|-----------------------------------|------------------------------------------|
| Initial Access     | T1190        | Exploit Public-Facing Application | Unvalidated input in `/ping`             |
| Execution          | T1059        | Command and Scripting Interpreter | Use of `eval()` in `/calculate`          |
| Persistence        | T1525        | Implant Container Image           | No image signing or registry validation  |
| Privilege Escalation | T1611      | Escape to Host                    | Running container as root                |
| Defense Evasion    | T1211        | Exploitation for Defense Evasion | Mutable filesystem; no read-only flags   |
| Impact             | T1499        | Endpoint Denial of Service        | Ping flooding or abuse of shell commands |

---

## 4. Controls Mapping

| Issue                      | Recommended Control                         | Framework Reference                   |
|----------------------------|---------------------------------------------|----------------------------------------|
| Hardcoded secrets          | Use `.env` with Compose or secrets manager  | NIST 800-53: SC-12, SC-28              |
| Root container user        | Add `USER appuser` + `no-new-privileges`    | NIST 800-53: AC-6, CM-6                |
| Lack of resource controls  | Add `mem_limit`, `pids_limit`               | NIST 800-53: SC-5, SC-6                |
| Exposed ports              | Bind to `127.0.0.1`, use firewalls/networks | NIST 800-53: SC-7                      |
| Mutable filesystem         | Use `read_only: true` in Compose            | CIS Docker Benchmark, SC-28            |
| Missing health check       | Add Docker `HEALTHCHECK`                    | CIS Docker Benchmark                   |
| Unsafe expression eval     | Replace `eval` with `ast.literal_eval`      | OWASP Top 10: A1-Injection             |
| Insecure subprocess calls  | Use `subprocess.run` safely without `shell` | OWASP Top 10: A1-Injection             |

---

## 5. Risk Rating Summary

| Threat               | Risk  | Likelihood | Impact    | Mitigation Priority |
|----------------------|-------|------------|-----------|----------------------|
| Command Injection    | High  | High       | Critical  | Immediate            |
| Credential Exposure  | Medium| High       | Medium    | High                 |
| Unsafe `eval()`      | High  | Medium     | High      | Immediate            |
| Root user in container | High| Medium     | Critical  | Immediate            |
| Missing logging      | Medium| Medium     | Medium    | Medium               |
| Lack of resource limits | Medium | Medium | High      | High                 |

---

## 6. Conclusion

This threat model identifies and addresses critical security issues in the Dockerized Python application, including unsafe input handling, excessive privileges, and lack of container hardening. Remediations include secure defaults (`read_only`, `cap_drop`, `USER`), input validation, and removal of risky operations like `eval`. Applying these changes significantly reduces the app’s attack surface and aligns it with best practices from OWASP, MITRE ATT&CK, and NIST 800-53.

