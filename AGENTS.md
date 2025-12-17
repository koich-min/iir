# AGENTS.md

## Repository
home/iir

## Project Name
iir — Internal Info Replacement

---

## What This Project Is

**iir** is a system for deterministic replacement of internal identifiers
before information is shared outside of a trusted boundary.

It replaces internal names (users, hosts, services, domains, and arbitrary
internal words) with stable, meaningful pseudonyms while preserving the
structure and intent of the original text.

---

## What This Project Is NOT

iir is **not** defined by a single execution model.

Although it *can* operate as a proxy in some configurations,
**proxy behavior is only one possible execution mode**, not the core concept.

The core concept is **replacement**, not mediation.

---

## Core Philosophy

> Humans will make mistakes.  
> Safety must be structural, not procedural.

This project assumes:
- Internal text will be copied
- Logs will be shared
- AI tools will be used

The system must remain safe even when users forget to sanitize data manually.

---

## Replacement Policy

### Matching Rules

- **Exact match only**
- No partial matches
- No regular expressions
- No heuristic or fuzzy matching

False positives are more dangerous than missed replacements.

---

### Replacement Order

- Replacement MUST be applied from **longest string to shortest**
- This prevents substring collisions

Example:
- Replace `srv-prod-01` before `srv`

---

## Pseudonym Rules

Pseudonyms are deterministic and derived from Django model IDs.

### Format

| Category | Pseudonym Example |
|--------|-------------------|
| Host | Host12 |
| Name | Name3 |
| Service | Service7 |
| Word | Word21 |

- The database `id` is the source of truth
- IDs are stable
- Logical deletion is preferred
- Re-numbering is discouraged

Pseudonyms are designed to preserve meaning, not to redact.

---

## Domains and Similar Identifiers

Domain names, FQDNs, and similar identifiers are considered **internal
information** and SHOULD be registered in the dictionary when needed.

They are treated as **normal dictionary entries** and follow the same rules:

- Exact match only
- No special parsing
- No URL or email decomposition

This avoids unnecessary complexity and prevents unintended replacements.

---

## Data Model (Conceptual)

Each dictionary entry must include:

- Category (Host / Name / Service / Word / etc.)
- Internal value (exact match target)
- Active flag (logical deletion)
- Timestamps

The dictionary database is a **highly sensitive internal asset**.

---

## Execution Modes (Non-Exclusive)

iir may be executed in multiple modes:

- Web application (form-based replacement)
- CLI filter (stdin → stdout)
- HTTP-based service
- MCP adapter (LLM safety layer)

No single execution mode defines the system.

---

## Security Boundaries

### Dictionary Access

- Dictionary data MUST NOT be exposed externally
- Authentication is mandatory for management interfaces
- Mapping rules must never appear in output

### Replacement Logs

- Logging replaced content is discouraged
- If logging is enabled, logs MUST contain only pseudonymized data
- Raw internal identifiers must never be logged

### External Output

- External output MUST NOT explicitly state that replacement occurred
- Category-based pseudonyms provide sufficient context

---

## Performance Philosophy

Usability depends on speed.

Initial implementation guidelines:
- Prefer simple, deterministic replacement
- Avoid premature optimization
- Optimize only after correctness is proven

Future improvements may include:
- In-memory dictionary snapshots
- Multi-pattern matching algorithms
- Streaming replacements for large inputs

Correctness and safety always take priority.

---

## Contribution Rules

Any change affecting replacement logic MUST include:

- Tests for overlapping entries
- Tests for substring collision prevention
- Tests across multiple categories

Changes that introduce partial matching are **not acceptable**.

---

## Guiding Principle

> Do not rely on users to remember rules.  
> Encode safety into the system.

