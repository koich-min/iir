# Container / Shared Mode - Running iir as a Boundary Safety Layer

This document describes how to run iir in **Container / Shared Mode**.

This mode is intended for shared environments, team usage, and organizational boundaries, where iir serves as a common safety layer between internal and external information.

This document assumes that you are already familiar with the Local / Personal Mode described in the quickstart guide.

---

## Purpose of Container / Shared Mode

Container / Shared Mode exists to establish a clear trust boundary between internal systems and external consumers.

Typical use cases:

- A central replacement service before data is shared outside the organization
- A Web-based manual inspection and replacement tool
- An HTTP API for internal automation
- An MCP adapter acting as an LLM safety layer

This mode is not intended for adu-hoc CLI use or personal pipelines.

---

## Design Principles

Container / Shared Mode follows these principles:

- Container-first design: the container defines the boundary
- Explicit configuration: no auto-detection or implicit fallbacks
- External database: dictionary is a persistent shared asset
- Non-reversibility: output is assumed to be permanently external
- Minimal behavior: the container does not attempt to be "smart"

---

## Deployment Overview

> Note:
> For local or private evaluation using Docker, see `docs/quickstart-docker.md`.
> This document focuses on **shared / boundary deployments** and does not describe
> evaluation-only setups.

While Container / Shared Mode is typically deployed with an external database
(PostgreSQL or MySQL), a SQLite-based setup may be used for evaluation,
testing, or small-scale shared environments.

In such cases, the database location must be explicitly configured
via environment variables and persistent storage.


Common components:

- iir container image
- External database (PostgreSQL or MySQL)
- Authentication and access control layer

---

## Configuration

Container / Shared Mode is configured exclusively via environment variables.

Basic configuration:

DB_ENGINE=postgresql
DB_NAME=iir
DB_USER=iir
DB_PASSWORD=secret
DB_HOST=db-postgres
DB_PORT=5432

### SQLite-based configuration (minimal setup)

For evaluation or small shared deployments, SQLite may be used.

In this case, the database location must be explicitly specified:

```text
DB_ENGINE=sqlite
SQLITE_PATH=/data/db.sqlite3
```

The database path must be backed by persistent storage.

---

## Web Replace Form

Browser-based access to the replacement functionality.

This interface is intended for:

- Manual inspection before external sharing
- Human verification of replacement behavior

It is not designed for high-volume automation.

---

## HTTP API

The HTTP API provides programmatic access to the replacement functionality.

It is intended for information systems, pipelines, and automated workflows.

Authentication is required.
All output must be treated as external.

---

## MCP Adapters

MCP adapters are an optional execution mode that allows iir to be used as a safety layer for LLMs.

The adapter runs iir inside a container and exposes a controlled interface for replacement.

This mode is especially useful when integrating with AI tools or automated prompt pipelines.

---

## Security Considerations

Container / Shared Mode requires additional security considerations:

- Dictionary data must be protected and never exposed directly
- Authentication and authorization are mandatory
- Raw internal identifiers must never be logged
- All replaced output must be considered external

---

## Relationship to Local Mode

Container / Shared Mode complements Local / Personal Mode:

- Local Mode is optimized for individual use
- Container Mode is optimized for shared boundaries
- They share the same replacement rules and dictionary schema

Do not attempt to use Container Mode as a replacement for Local Mode workflows.

They are complementary, not interchangeable.

