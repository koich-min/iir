# Quickstart – Running iir Locally

This document provides a minimal quickstart for running
iir locally for evaluation or internal use.

It is intended for users who are not familiar with Django
internals, but are comfortable with command-line tools.

This guide focuses only on getting iir running and
performing a basic replacement.

For design rationale and security constraints, see AGENTS.md.

---

## Prerequisites

- Python 3.11 or newer
- `git`
- A command-line shell

"Pipenv" is used in the examples below,
but any virtual environment tool is ok.

---

## Get the Code

Clone the repository and enter the project directory.

git clone <repository-url>
cd iir

---

## Set up the Environment

Install dependencies and activate the environment.

pipenv install
pipenv shell

Alternatively, you may use venv/pip directly.

---

## Initialize the Database

Run the database migrations.

python manage.py migrate

---

At this point, iir is ready to run.

## Register Your First Entry

iir does not auto-discover internal identifiers.
All replacements are explicit and human-curated.

Register an example entry using the CLI.

echo "srv-prod-01" | iir add-entry HOST

---

## Perform a Replacement

Now perform a basic replacement using stdin → stdout.

echo "connect to srv-prod-01" | iir replace

You should see the host name replaced with a deterministic pseudonym (e.g. Host12).

---

## Web Replace Form (Optional)

iir also provides a simple Web interface for manual inspection.

Start the development server:

python manage.py runserver

The web replace form is available at a known URL.
It is intended for human verification only and is not
required for normal CLI usage.

---


## API Access (Optional)

iir exposes an authenticated HTTP API for internal use
(automation, integration, or infrastructure).

API usage is not required for basic operation.
For details and verification examples, see docs/api.md.

---

## Next Steps

- Register additional entries that reflect your internal environment
- Integrate iir into existing pipelines using the CLI
- Review AGENTS.md for design constraints and contribution rules

When ready, you may explore other execution modes
such as the HTTP API or MCP adapters.
