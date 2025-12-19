# Quickstart – Running iir Locally (Local / Personal Mode)

This document provides a minimal, **verified** quickstart for running **iir** locally
for evaluation or personal use.

It corresponds to the **Local / Personal Mode** described in the main README.

This guide assumes:
- a local or private environment
- CLI-based usage
- no prior knowledge of Django internals

It focuses only on getting iir running and confirming that replacement works.

For design rationale and security constraints, see **AGENTS.md**.

---

## Prerequisites

- Python **3.12 or newer**
- `git`
- `pipenv`
- A POSIX-compatible shell (bash / zsh)

---

## Get the Code

Clone the repository and enter the project directory:

```sh
git clone <repository-url>
cd iir
```

---

## Set up the Environment

Create a virtual environment and install dependencies:

```sh
pipenv install
pipenv run pip install -e .
pipenv shell
```

At this point, the `iir` CLI command should be available.

---

## Initialize Development Secrets

Generate a local development secret:

```sh
iir dev-init
```

This creates a `.env.secret` file in the project root.

The generated file uses quoted values and is safe to load in a shell.

---

## Load Environment Variables

Before running Django management commands, load the secret into your shell:

```sh
set -a
source .env.secret
set +a
```

This exports all variables defined in `.env.secret` and makes them available to Python and Django.

---

## Initialize the Database

Run database migrations:

```sh
python manage.py migrate
```

If this completes without errors, iir is ready to use.

---

## Register Your First Entry

iir does not auto-discover internal identifiers.
All replacements are explicit and human-curated.

Register a simple example entry:

```sh
echo "srv-prod-01" | iir add-entry HOST
```

---

## Perform a Replacement (CLI)

Test replacement using stdin → stdout:

```sh
echo "connect to srv-prod-01" | iir replace
```

Example output:

```
connect to Host1
```

(The number depends on your local database.)

---

## Web Replace Form (Optional)

For users who prefer a browser-based workflow, iir provides a simple Web UI.

Start the development server:

```sh
python manage.py runserver
```

Open the replace form in your browser:

```
http://localhost:8000/replace/
```

**Notes:**
- The trailing slash (`/replace/`) is required
- This interface is intended for manual inspection only

---

## API Access (Optional)

iir also exposes an authenticated HTTP API for internal use
(automation, integration, or infrastructure).

API usage is **not required** for basic operation.

See `docs/api.md` for details and verification examples.

---

## Next Steps

- Register additional entries that reflect your internal environment
- Integrate iir into existing pipelines using the CLI
- Review **AGENTS.md** for design constraints and contribution rules

When ready, you may explore other execution modes
such as the HTTP API or planned MCP adapters.

---

### Verified Scope

This quickstart has been validated with:

- pipenv + editable install
- `iir dev-init`
- `.env.secret` shell loading
- database migration
- CLI replacement
- Web replace form (`/replace/`)
