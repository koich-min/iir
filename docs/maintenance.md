# Maintenance Guide

This document describes **maintenance and administrative workflows** for iir.

It is intended for **developers and operators**, not for everyday CLI usage.
If you only want to try iir quickly, see `docs/quickstart.md`.

---

## Scope and responsibility

iir provides **structural safety** for replacing internal identifiers.
It does **not** guarantee semantic preservation or explainability of outputs.

As a result:

- Replacement behavior is deterministic and simple
- Meaning degradation is expected and accepted
- Operational responsibility lies with the operator

This document explains **explicit, operator-driven actions**
that are intentionally **not automated**.

---

## Development initialization (`iir dev-init`)

```sh
iir dev-init
```

This command initializes a **local state directory** for iir.

It performs the following actions:

- Creates `.env.secret` if it does not already exist  
  (contains `DJANGO_SECRET_KEY`, written with shell-safe quoting)
- Creates `db.sqlite3`
- Runs Django migrations against that database

### State directory resolution

- If `DATA_DIR` is **not set**:
  - The current working directory is used
- If `DATA_DIR` **is set**:
  - That directory is used as the state directory
  - The directory **must already exist**

After running `dev-init`, the state directory will contain:

```text
.env.secret
db.sqlite3
```

These files are **local development artifacts** and must not be committed.

---

## Environment variables

### `.env.secret`

`.env.secret` contains the Django secret key:

```text
DJANGO_SECRET_KEY="random-secret-value"
```

Notes:

- Values are **double-quoted** to remain safe when sourced by a shell
- The file is intended for **local or controlled use only**
- iir CLI commands load this file automatically when required

---

### SQLite database location

When using SQLite (default):

- The database file is `db.sqlite3` in the **state directory**
- The state directory is determined by:
  - `DATA_DIR` if set
  - otherwise the current working directory

Django maintenance commands must use the same database via `SQLITE_PATH`:

```sh
export SQLITE_PATH="${DATA_DIR:-$(pwd)}/db.sqlite3"
```

---

## Administrative commands (CLI)

Administrative actions are intentionally **explicit and operator-driven**.

They define trust boundaries and therefore are **not automated**.

### Create an admin user

```sh
iir admin createsuperuser
```

Notes:

- Interactive by design
- Writes directly to the configured database
- No credentials are stored in images or manifests

---

### Collect static files (Admin UI)

```sh
iir admin collectstatic --noinput
```

This is required when:

- Running Django Admin
- Static files are not baked into the image
- Using shared or container-based environments

---

### Run a local admin server

```sh
iir admin runserver
```

Optional address/port may be provided:

```sh
iir admin runserver 0.0.0.0:8000
```

This command launches the application via **uvicorn**
while preserving Django-compatible CLI syntax.

The Admin interface is available at:

```text
http://127.0.0.1:8000/admin/
```

This server is intended for **local or controlled environments only**.

---

## API token management

If API authentication is enabled, tokens must be issued explicitly.

### Create an API token

```sh
iir api create-token <username>
```

Notes:

- The user must already exist
- Tokens are printed to stdout
- Token issuance is a deliberate administrative action

This replaces manual token creation via Django shell.

---

## CLI vs maintenance responsibilities

- **CLI (`iir add-entry`, `iir replace`)**
  - Safe, incremental, append-style operations
- **Maintenance (this document)**
  - Administrative and trust-boundary operations

If an action can be performed via the normal CLI,
it does **not** belong in this document.

---

## Handling dictionary entries

Dictionary entries may be **edited or deleted via Django Admin**.

Common approaches:

- Logical deletion (`is_active = False`)
- Physical deletion (operator discretion)

Notes:

- iir does not guarantee explainability of past outputs
- Semantic degradation is already inherent to the model
- History retention is an **operational decision**

---

## Design notes

- iir prioritizes determinism and structural safety
- Administrative actions are explicit and auditable
- No reverse (de-anonymization) mechanism is provided
- The dictionary database is a sensitive internal asset

---

## Summary

- `iir dev-init` creates an explicit local state directory
- Administrative actions are performed via explicit CLI commands
- Django Admin is the supported interface for inspection and correction
- API tokens are issued intentionally and manually
- Convenience is traded for clarity and safety

