# Container / Shared Mode – Deploying iir

This document describes how to deploy **iir** in **Container / Shared Mode**
as a **persistent, shared safety layer** inside a private or organizational environment.

This mode is intended for **long-running deployments** where iir defines
a trust boundary between internal systems and external consumers.

Evaluation-only or ad-hoc Docker usage is **not covered here**.
For Docker-based evaluation, see:

- `docs/quickstart-docker.md`

---

## Assumptions

This document assumes that:

- You are familiar with the Local / Personal Mode
- You understand that Container / Shared Mode defines a trust boundary
- You intend to operate iir as a shared service

This document focuses on **deployment and operation**, not evaluation.

---

## Requirements

- Docker 20.10 or newer (or compatible container runtime)
- A container registry (public or private)
- A persistent external database (PostgreSQL or MySQL recommended)

SQLite may be used only for **small-scale shared environments or testing**.
It is **not recommended for production deployments**.

---

## Container Image

Most users should use a **pre-built container image**
published to a container registry (for example, Docker Hub).

The official image is designed to:

- Run as a non-root user
- Require explicit lifecycle commands
- Avoid implicit initialization or auto-migration

The container image does **not** define a default command.
This is intentional and forces explicit startup behavior.

---

## Building the Container Image (Optional)

Building the image yourself is **optional** and only required if you need:

- Custom patches
- Internal forks
- Modified dependencies

Example multi-architecture build using docker buildx:

```sh
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t your-registry/iir:0.1.14 \
  .
```

Most deployments should rely on a pre-built image instead of rebuilding.

---

## Environment Configuration

All configuration is provided via environment variables.

Example PostgreSQL configuration:

```text
DB_ENGINE=postgresql
DB_NAME=iir
DB_USER=iir
DB_PASSWORD=secret
DB_HOST=db-postgres
DB_PORT=5432
```

Configure these variables in:

- docker run
- docker-compose
- Kubernetes manifests

No configuration files are baked into the image.

---

## SQLite Configuration (Limited Use)

SQLite may be used for **small shared setups or testing**.

In this case, the database location must be explicitly specified:

```text
DB_ENGINE=sqlite
SQLITE_PATH=/data/db.sqlite3
```

The database path **must** be backed by persistent storage.

This configuration is **not an evaluation shortcut**.
For evaluation-only usage, use `docs/quickstart-docker.md`.

---

## Running the Container

The container does not automatically start any services.

You must explicitly specify the command to run,
for example when starting a web or API service.

This behavior is intentional and prevents accidental exposure.

---

## Database Migrations

Database migrations are a **separate operational step**.

The container does not automatically run migrations.
Run migrations manually or as a dedicated job during deployment:

- Initial deployment
- Schema upgrades
- Controlled maintenance windows

This ensures predictable and auditable changes.

---

## Security Notes

- Never bake environment variables or secrets into the image
- Treat all replaced output as external
- Protect the dictionary database as sensitive data
- Restrict access to administrative endpoints

Container / Shared Mode assumes a hostile external boundary.

---

## Relationship to Other Modes

Container / Shared Mode is complementary to other usage modes:

- Local / Personal Mode: individual CLI usage
- Docker Evaluation Mode: short-lived inspection and testing
- Container / Shared Mode: persistent boundary service

Do not use Container / Shared Mode for ad-hoc local workflows.

Each mode exists to support a distinct operational need.

