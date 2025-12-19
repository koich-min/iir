# iir — Internal Info Replacement

**iir (Internal Info Replacement)** is a lightweight system for safely replacing
internal identifiers (hosts, domains, service names, user names, etc.) before
sharing logs, documents, or prompts with external parties or AI systems.

It is designed as a **structural safety layer**:
even if humans forget to sanitize data manually, internal information should
not leak outside a trusted boundary.

---

## Two Usage Modes (Important)

iir explicitly supports two different usage modes.

They serve different purposes, and this distinction is intentional.

---

### 1. Local / Personal Mode (CLI-First)

This mode is intended for individual users, developers, and local workflows.

Typical use cases:
- Preparing logs or text before sharing
- Sanitizing prompts before sending them to AI tools
- Ad-hoc replacement in pipelines or scripts

Characteristics:
- CLI-first design (stdin „ stdout)
- Installed via pip (e.g. pip install -e .)
- Sqlite is acceptable for local use
- Django is an internal implementation detail (not a user concern)

---

### 2 Shared / Boundary Mode (API / Web / MCP)

This mode is intended for shared environments, team usage, and organizational boundaries.

For example:
- Recommended as a common safety layer before external data sharing
- Http-based replacement service
- Web-based manual inspection and replacement
- MCP adapter as an LLM safety layer

Characteristics:
- Container-first design (Docker / k8s)
- External database (PostgreSQL / MySQL)
- Dictionary is a central, sensitive asset
- Explicit authentication and access controls

This mode defines the trust boundary between internal and external information.

---

## Core Idea

The core idea of iir is intentionally simple:

- Maintain an explicit dictionary of internal identifiers
- Replace them deterministically with meaningful pseudonyms
- Never leak internal naming conventions outside

iir does not attempt to *discover* internal information.
All replacements are explicit, predictable, and auditable.

---

## Key Features

- Deterministic pseudonymization based on dictionary entries
- Exact-match replacement (no fuzzy or partial matching)
- Longest-first replacement to avoid substring collisions
- Categories are free-form and user-defined
- CLI-first design (stdin → stdout filter)
- Web-based replace form for manual inspection
- Designed to work with existing UNIX tools

---

## Core Concepts

### Entry

An **Entry** represents one internal identifier.

Each entry has:

- `category`: logical label (e.g. HOST, DOMAIN, SERVICE, WORD)
- `value`: the exact string to replace
- `is_active`: whether the entry participates in replacement

Categories are **labels only**.
They are not constrained or enforced by the system.

---

### Replacement Rules

- Only **exact string matches** are replaced
- Only **active** entries are used
- Longer values are replaced first to avoid collisions
- Pseudonyms are generated as: `<Category><id>`

Example:

- HOST:srv-prod-01 → Host12

---

## Basic Usage (CLI – Recommended)

iir provides a standalone CLI entry point.

### Replace text (stdin → stdout)

```bash
echo "connect to my.domain" | iir replace
```

This is the primary and recommended usage pattern.
Options allow limiting or excluding categories as needed.

### Register entries (stdin)

```bash
echo "srv-prod-01" | iir add-entry HOST
```

Duplicate entries are ignored safely.
This design allows iir to integrate naturally with existing UNIX pipelines.

## Registering Entries (Examples)

### Import domain from echo

```bash
echo "my.domain" | iir add-entry DOMAIN
```

### Example: Import hosts from DNS (AXFR)

If your internal DNS allows zone transfer:

```bash
dig axfr my.domain @dns-server \
  | awk '{print $1}' \
  | sed 's/\.$//' \
  | sort -u \
  | iir add-entry HOST
```

Notes:

- Only names are imported (IPs are ignored)
- Trailing dots from FQDNs are removed
- Review entries in Django admin if needed

## Web Usage Modes

### Replace Form

The Web UI provides a simple form-based replacement interface.

- Paste text to be replaced
- Categories are derived from existing Entry data
- All categories are selected by default
- Unchecked categories are ignored

This mode is intended for:

- Manual inspection
- Preparing logs for external sharing
- Sanitizing text before sending to AI tools

---

## Non-Reversibility Policy

iir intentionally does not provide a reverse (de-pseudonymization) feature.

Once text is replaced, it is assumed to be shared outside of the internal boundary.
Providing automated reversal would encourage unsafe workflows and increase the risk of accidental data leakage.

If reverse lookup is ever required, it must be performed manually using the internal dictionary database, not automated tools.

---

## Design Philosophy

- iir does not auto-discover identifiers
- All entries are explicit and human-curated
- Existing UNIX tools are preferred over custom scanners
- Replacement accuracy is prioritized over coverage

This keeps the dictionary trustworthy and predictable.

---

## Security Considerations

- Dictionary data is never exposed externally
- Replacement rules are internal-only
- Pseudonyms are deterministic but non-reversible without the database
- No original identifiers appear in output
- Designed as a safety layer before external sharing or AI usage

---

## Development Notes

- Framework: Django
- Dictionary stored in a database
- CLI entry point bootstraps Django explicitly
- Intended for containerized / k8s environments
- Minimal dependencies by design

For deeper design rationale and constraints, see AGENTS.md.

---

## Administration

For initial administrative setup (creating superuser, issuing tokens),
see [Initial Administrative Setup](docs/initial-admin.md).

---

## What should be registered as Entry?

The following categories are commonly useful as an initial set.
They are examples, not requirements.

| Category | Examples | Reason |
|---|---|---|
| HOST | vm014, db-prod-01 | Reveals infrastructure structure |
| DOMAIN | my.domain | Exposes internal network boundary |
| NAME | deploy, admin, koich | Identifies users or service accounts |
| SERVICE | auth-service, billing-api | Reveals system architecture |
| WORD | prod, staging | Leaks environment or operational context |

As a general rule, register any value that could allow a third party to
infer internal structure, roles, or access patterns.

---

### Links

- [quickstart](docs/quickstart.md)  
  Minimal guide for running iir locally in **Local / Personal Mode** (CLI-first).

- [Container / Shared Mode](docs/container-mode.md)  
  Running iir as a **shared boundary safety layer** using containers (API / Web / MCP).

- [api](docs/api.md)  
  Internal HTTP API usage and verification examples.

- [operations](docs/operations.md)
  For advanced bootstrap or migration scenarios, see developer documentation.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

