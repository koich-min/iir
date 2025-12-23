# iir — Internal Info Replacement

**iir (Internal Info Replacement)** is a lightweight system for safely replacing
internal identifiers (hosts, domains, service names, user names, etc.) before
sharing logs, documents, or prompts with external parties or AI systems.

It is designed as a **structural safety layer**:
a tool that helps humans safely sanitize (replace) internal identifiers
before sharing information outside a trusted boundary.


---

## Intended usage note

iir is designed to be used **inside a local or private environment**
such as a developer machine, LAN, or internal network,
as a preprocessing tool **before** sharing text with external services
(including public or hosted LLMs).

iir itself is **not intended to be exposed as a public service**.
How and where it is operated is the responsibility of the user.

Please note that the dictionary used by iir should be treated as **your private internal data**.
Depending on how entries are curated, it can easily become sensitive or security-relevant information.

iir is a utility to assist safe replacement workflows.
It does not claim to provide complete security guarantees.

---

## About MCP integration

MCP support is planned as an **optional execution mode** for iir.
It is primarily intended for **on-premise or self-hosted LLM setups**,
where model outputs need to be sanitized before being exposed externally.

MCP integration does not change the core concept of iir.
Replacement logic and safety assumptions remain the same,
and MCP is **not required** for using iir effectively.

---

## Installation

```sh
pip install iir-tool
```

> Note: The PyPI package name is `iir-tool`, but the CLI command is `iir`.

---

## Two Usage Modes (Important)

iir supports two complementary usage modes.


### 1. Local / Personal Mode (CLI-First)

Designed for individual users and local workflows.

Typical uses cases:
- Preparing logs or text before sharing
- Sanitizing prompts before sending to AI tools
- Ad-hoc replacement in pipelines or scripts

Characteristics:
- CLI-first design (stdin → stdout)
- Simple installation (extra config not required)
- Suitable for quick evaluation via quickstart

### 2. Shared / Boundary Mode (API / Web / MCP)

This mode is intended to be deployed **inside a LAN or private environment**
and to act as a boundary **before** data is shared with external services.
It is **not designed or recommended to be operated as a publicly exposed service**.

This mode is commonly used in shared environments, team usage, and organizational boundaries.

Examples:
- HTTP based replacement service (for internal use)
- Web based replacement form for manual inspection
- MCP adapter as an optional LLM safety layer

---

## Basic Usage (CLI, Recommended)

## Development initialization (`dev-init` / `dev-remove`)

For local development and evaluation, iir provides explicit helper commands
to initialize and clean up the working directory.

### `iir dev-init`

```sh
iir dev-init
```

This command performs the following actions **in the current directory**:

- Creates `.env.secret` if it does not already exist  
  (contains `DJANGO_SECRET_KEY` for local use)
- Creates `db.sqlite3` in the current directory (SQLite)
- Runs Django migrations against that database

After running `dev-init`, the directory will contain:

```text
.env.secret
db.sqlite3
```

These files are **local development artifacts** and should normally be
excluded from version control.

### `iir dev-remove`

```sh
iir dev-remove
```

This command removes `.env.secret` from the current directory.

Notes:

- `dev-remove` does **not** delete `db.sqlite3`
- Database removal is intentionally left to the user
- This avoids accidental data loss

### Important notes

- `dev-init` and `dev-remove` are **explicit developer helpers**
- iir will **never** create or migrate databases implicitly during
  normal commands such as `replace`
- Database initialization is always a deliberate action

This design keeps database state predictable and avoids unintended
side effects.


```sh
echo "my.domain" | iir add-entry DOMAIN
echo "connect to my.domain" | iir replace
```

---

## Links

- [quickstart](docs/quickstart.md)
- [Container / Shared Mode](docs/container-mode.md)
- [api](docs/api.md)

---

## License

This project is licensed under the [MIT License](LICENSE).

