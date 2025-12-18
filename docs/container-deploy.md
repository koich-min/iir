# Container / Shared Mode - Deploying iir in a Home Infrastructure

This document describes how to deploy iir in **Container / Shared Mode** for a private or home environment.

The goal is to run iir as a persistent, shared safety layer, using containers and an external database.

This document assumes:

- You have already read the quickstart guide (Local / Personal Mode)
- You understand that Container / Shared Mode defines a trust boundary

---

## Requirements


- Docker (20.10 or newer)
- Docker buildx (for multi-arch builds, optional)
- A container registry (private or public)
- PostgreSQL or MySQL running externally

---

## Building the Container Image

Iir does not prescribe a single build flow, but the recommended approach is to build a multi-architecture image using docker buildx.

Example build command:

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t your-registry/iir:0.1.0 \
  .

This creates a single image that can be used on both x86_64 and ARM64 environments.

---

## Environment Configuration

All configuration is provided via environment variables.

Basic example:

DB_ENGINE=postgresql
DB_NAME=iir
DB_USER=iir
DB_PASSWORD=secret
DB_HOST=db-postgres
DB_PORT=5432

Configure those variables in your docker run command,
docker-compose.yml, or Kubernetes manifests.

---

## Running the Container

The Dockerfile does not define a default command.
This is intentional.

Example for running a web/api service:
  
Ensure you specify the start command explicitly, for example in Kubernetes or docker-compose.

---

## Database Migrations

Database migrations are a separate operational step.

The container does not automatically run migrations.
Run them manually or as a separate job when deploying.

---

## Security Notes

- Never include env files in the image
- Treat all output as external
- Protect access to the dictionary database

---

## Relationship to Local Mode

Container / Shared Mode is complementary to Local / Personal Mode.

Do not attempt to use this mode for ad-hoc local workflows.

