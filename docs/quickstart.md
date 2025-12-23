# Quickstart – Running iir Locally (CLI)

This document provides a minimal, **verified** quickstart for running **iir**
locally in **Local / Personal Mode**.

It focuses only on confirming that:

- iir installs correctly
- the CLI works
- deterministic replacement behaves as expected

No knowledge of Django internals is required.

For maintenance, inspection, or administrative workflows,
see `docs/maintenance.md`.

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

Confirm the CLI is available:

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
- Creates `db.sqlite3` in the current directory
- Runs database migrations

No additional setup is required.

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
- CLI-based entry registration
- CLI-based replacement

