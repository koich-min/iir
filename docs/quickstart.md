# Quickstart – Running iir Locally (CLI)

This document provides a minimal, **verified** quickstart for running **iir**
locally in **Local / Personal Mode (CLI-first)**.

It focuses only on confirming that:

- iir installs correctly via PyPI
- the CLI works as expected
- deterministic replacement behaves correctly

This quickstart assumes **direct CLI usage** and does **not** cover
Docker or container-based execution.

For container-based evaluation or deployment scenarios,
refer to the Docker-specific documentation linked from the README.

---

## Prerequisites

- Python **3.12 or newer**
- A POSIX-compatible shell (bash / zsh)

---

## Install iir

Install iir from PyPI:

```sh
pip install iir-tool
```

Confirm that the CLI is available:

```sh
iir version
```

---

## Initialize local state

Before first use, initialize the local working directory:

```sh
iir dev-init
```

This command:

- Creates `.env.secret` (if missing)
- Prepares local state files

It does **not** run database migrations.

If the environment variable `DATA_DIR` is set, iir will use that directory
instead of the current working directory to store local state.
This is optional for direct CLI usage.

---

## Run database migrations

After initialization, you must explicitly run database migrations:

```sh
iir admin migrate
```

This step initializes the database schema required by iir.

---

## Register your first entry

iir replaces only explicitly registered values.

Add a simple example entry:

```sh
echo "srv-prod-01" | iir add-entry HOST
```

---

## Perform a replacement

Run a replacement using stdin → stdout:

```sh
echo "connect to srv-prod-01" | iir replace
```

Example output:

```text
connect to Host1
```

(The number depends on your local database.)

---

## What’s next

You have confirmed that:

- iir is installed correctly
- the CLI works
- database initialization is explicit and controlled
- replacement is deterministic

From here, you may:

- Register additional entries
- Integrate iir into scripts or pipelines
- Explore maintenance and inspection workflows

For administrative tasks such as entry inspection, correction,
or Django Admin usage, see:

- `docs/maintenance.md`

---

## Verified scope

This quickstart has been validated with:

- `pip install iir-tool`
- `iir dev-init`
- `iir admin migrate`
- CLI-based entry registration
- CLI-based replacement

