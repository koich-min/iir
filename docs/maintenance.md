# Maintenance Guide

This document describes **maintenance and inspection workflows** for iir.
It is intended for **developers and operators**, not for everyday CLI usage.

If you only want to try iir quickly, see `docs/quickstart.md` instead.

---

## Scope and responsibility

iir provides **structural safety** for replacing internal identifiers.
It does **not** guarantee semantic preservation or explainability of outputs.

As a result:

- Replacement behavior is deterministic and simple
- Meaning degradation is expected and accepted
- Operational responsibility lies with the operator

This document explains how to perform maintenance tasks
with those assumptions in mind.

---

## Development initialization (`iir dev-init`)

```sh
iir dev-init
```

This command performs the following actions **in the current directory**:

- Creates `.env.secret` if it does not already exist  
  (contains `DJANGO_SECRET_KEY`, written with shell-safe quoting)
- Creates `db.sqlite3` in the current directory
- Runs Django migrations against that database

After running `dev-init`, the directory will contain:

```text
.env.secret
db.sqlite3
```

These files are **local development artifacts** and should not be committed.

---

## Environment variables

### `.env.secret`

`.env.secret` contains the Django secret key:

```text
DJANGO_SECRET_KEY="random-secret-value"
```

Notes:

- Values are **double-quoted** to remain safe when sourced by a shell
- The file is intended for **local use only**
- iir CLI commands load this file automatically when required

---

### SQLite database location

When using SQLite (default):

- The database file is `db.sqlite3` in the current directory
- Django maintenance commands must use the same database via `SQLITE_PATH`

---

## Django maintenance commands

Django management commands are used **only for maintenance tasks**,
such as inspection, correction, or cleanup of dictionary entries.

Before running any Django command, export environment variables:

```sh
set -a
source .env.secret
set +a
export SQLITE_PATH="$(pwd)/db.sqlite3"
```

---

### Create admin user

```sh
DJANGO_SETTINGS_MODULE=svr.settings python -m django createsuperuser
```

---

### Collect static files (Admin UI)

```sh
DJANGO_SETTINGS_MODULE=svr.settings python -m django collectstatic
```

---

### Run Django development server

```sh
DJANGO_SETTINGS_MODULE=svr.settings python -m django runserver
```

The Admin interface is available at:

```text
http://127.0.0.1:8000/admin/
```

This server is intended for **local, non-public use only**.

---

## Handling dictionary entries

### CLI vs maintenance responsibilities

- Adding entries and running replacements are performed via the **iir CLI**
- Inspection, correction, and cleanup are performed via **Django Admin**

The CLI is intentionally limited to **append-style operations**.

---

### Mistaken or obsolete entries

Dictionary entries may be **edited or deleted via Django Admin**.

In many cases, disabling an entry by setting `is_active = False`
is sufficient and convenient.

Physical deletion is also permitted and left to **operator discretion**.

Notes:

- iir does not guarantee explainability of past outputs
- Semantic degradation is already inherent to the replacement model
- Decisions about history retention are an **operational concern**

---

## Design notes

- iir prioritizes simplicity and determinism over semantic fidelity
- The dictionary database is treated as an internal operational asset
- No reverse (de-anonymization) mechanism is provided by design
- Maintenance actions are explicit and operator-driven

---

## Summary

- `iir dev-init` creates an explicit local development state
- Normal CLI usage does not modify database structure
- Django Admin is the supported interface for maintenance
- Entry deletion or deactivation is an operational choice
- iir provides structure; operators provide judgment

