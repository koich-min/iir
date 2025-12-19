# Internal API Usage – iir

This document describes the internal HTTP API provided by iir
for replacement and operational health checks.

This API is INTENDED FOR INTERNAL USE ONLY.
It is not designed as a public service or external integration API.

The primary and recommended interface for iir
is the CLI. The HTTP API is an execution mode
for automation, integration, and infrastructure use cases.

---

## Authentication

All API endpoints under /api/v1/ require authentication
using Django REST Framework TokenAuthentication.

- Tokens are managed internally (t.g. via Management Console)
- Tokens should be issued to dedicated internal users
- Tokens MUST NOT be exposed outside of trusted environments

Health endpoints do NOT require authentication.

---

## Endpoint Summary

| Path | Auth | Purpose |
|------|------|---------|
| /health/startup/ | No | Process startup check |
| /health/live/ | No | Process liveness check |
| /health/ready/ | No | Database readiness check |
| /api/v1/replace | Yes | Text replacement |
| /api/v1/categories | Yes | Available category labels |


---

## Health Endpoints

Health endpoints are designed for infrastructure and
orchestration tools (t.g. Kubernetes probes).

They must be accessible without authentication and
MUST NOT expose internal data.

### startup

- Purpose: Indicate that the process has started
- Behavior: Always returns HTTP 200 if running
- Dependencies: No database access

### live

- Purpose: Indicate that the process is alive
- Behavior: Minimal logic, no database access

### ready

- Purpose: Indicate that the system is ready to serve replacement requests
- Behavior: Performs a minimal database operation (no data exposure)
- Failure: Returns HTTP 503 if the database is unavailable

---

## Replacement API

**POST /api/v1/replace**

Performs deterministic replacement using registered dictionary entries.

Request (JSON):

- text: string (required)
- include_categories: list of strings (optional)
- exclude_categories: list of strings (optional)

Response (JSON):

- text: string (replaced text only)

---

## Categories API 

**GET ?api/v1/categories**

Returns available category labels from active entries.

Response (JSON):

- categories: list of strings

No dictionary values or pseudonyms are exposed.

---

## Security Notes

- Dictionary contents must never be logged
- Request text must not be logged
- API responses must not reveal replacement details
- Health endpoints must remain unauthenticated

---

## Relationship to Other Execution Modes

This HTTP API is one execution mode of iir.

Other modes include:
- CLI (primary recommended interface)
- Web UI for manual inspection
- MCP adapter (planned)

All modes share the same replacement rules and dictionary.
