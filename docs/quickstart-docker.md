# Quickstart – Evaluating iir with Docker

This document provides a **verified evaluation flow** for running **iir**
using the official Docker image.

This quickstart is intended for:

- Local or private evaluation
- Inspecting iir behavior before adoption
- Non-production usage

It is **not** intended for public exposure or long-running shared services.

For CLI-based local usage (pip install),
see `docs/quickstart.md`.

For shared or boundary deployments,
see `docs/container-mode.md`.

---

## Prerequisites

- Docker (or compatible container runtime)
- A POSIX-compatible shell (bash / zsh)

---

## Evaluation model

Docker-based evaluation differs from direct CLI usage:

- Commands are executed via `python -m iir`
- State is stored in a volume-mounted directory
- Django lifecycle operations are **explicit and manual**

There is **no implicit setup**.
Each step must be run intentionally.

---

## 1. Prepare local state directory

Choose or create a directory on the host to store iir state:

- `.env.secret`
- database file
- other local state

This example uses the current directory:

```sh
mkdir -p ./data
```

---

## 2. Initialize state files

Initialize the state directory:

```sh
docker run --rm \
  -v "$(pwd)/data:/data" \
  -e DATA_DIR=/data \
  koich/iir:latest \
  python -m iir dev-init
```

This step:

- Creates `.env.secret` (if missing)
- Prepares state files

It does **not** run database migrations.

---

## 3. Run database migrations

After initialization, run migrations explicitly:

```sh
docker run --rm \
  --env-file ./data/.env.secret \
  -v "$(pwd)/data:/data" \
  -e DATA_DIR=/data \
  koich/iir:latest \
  python -m iir admin migrate
```

---

## 4. Create admin user (interactive)

To access Django Admin, create an admin user.
This step requires a TTY:

```sh
docker run --rm -it \
  --env-file ./data/.env.secret \
  -v "$(pwd)/data:/data" \
  -e DATA_DIR=/data \
  koich/iir:latest \
  python -m iir admin createsuperuser
```

---

## 5. Collect static files

Prepare static files for the admin interface.

Create a directory on the host for static files:

```sh
mkdir -p ./staticfiles
```

Then run:

```sh
docker run --rm \
  --env-file ./data/.env.secret \
  -v "$(pwd)/data:/data" \
  -v "$(pwd)/staticfiles:/app/staticfiles" \
  -e DATA_DIR=/data \
  koich/iir:latest \
  python -m iir admin collectstatic
```

---

## 6. Run the development server

Start the development server:

```sh
docker run --rm \
  --env-file ./data/.env.secret \
  -v "$(pwd)/data:/data" \
  -v "$(pwd)/staticfiles:/app/staticfiles" \
  -e DATA_DIR=/data \
  -p 8000:8000 \
  koich/iir:latest \
  python -m iir admin runserver 0:8000
```

The admin interface will be available at:

- http://localhost:8000/admin/

---

## Notes

- This Docker image uses **SQLite by default** for evaluation.
- All Django operations are explicit and opt-in.
- State must be persisted via volume mounts.
- This setup is **not intended for public or production use**.

---

## Verified scope

This quickstart has been validated with:

- Docker Hub image (`koich/iir`)
- `dev-init`
- `admin migrate`
- `admin createsuperuser`
- `admin collectstatic`
- `admin runserver`

