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

The primary goal is **structural safety**:  
internal information must not leak even when humans make mistakes.

---

## What This Project Is NOT

iir is **not** defined by a single execution model.

Although it *can* operate as a proxy in some configurations,
**proxy behavior is only one possible execution mode**, not the core concept.

The core concept is **replacement**, not mediation.

iir is also **not** a redaction tool:
- Data is not removed
- Data is not masked
- Meaning is preserved through pseudonyms

---

## Core Philosophy

> Humans will make mistakes.  
> Safety must be structural, not procedural.

This project assumes:
- Internal text will be copied
- Logs will be shared
- Commands will be piped
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
| Domain | Domain5 |

- The database `id` is the source of truth
- IDs are stable
- Logical deletion is preferred
- Re-numbering is discouraged

Pseudonyms are designed to preserve meaning, not to redact.

---

## Non-Reversibility Policy

iir **intentionally does not provide a reverse (de-anonymization) mechanism**.

This is a deliberate security decision:
- Reverse mappings encourage unsafe workflows
- Storing or exposing reverse logic increases blast radius
- External outputs must be treated as permanently detached from internal data

If reverse lookup is required, it must occur **outside of iir** under
strictly controlled internal procedures.

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

Each dictionary entry includes:

- Category (free-form label)
- Internal value (exact match target)
- Active flag (logical deletion)
- Timestamps

### Category Design

- Categories are **labels**, not enforced types
- No fixed enum or hard-coded list
- Users may add, remove, or rename categories freely
- The system does not assume semantic meaning beyond labeling

This allows the dictionary to evolve with real-world usage.

The dictionary database is a **highly sensitive internal asset**.

---

## Execution Modes (Non-Exclusive)

iir supports multiple execution modes:

- Web application (form-based replacement)
- CLI filter (stdin → stdout)
- CLI entry point (`iir replace`)
- HTTP-based service
- MCP adapter (LLM safety layer)

No single execution mode defines the system.

All modes share the same replacement rules and dictionary.

---

## CLI and Django Relationship

iir is implemented as a Django project internally, but:

- The Django project itself is not packaged or distributed
- The CLI entry point (`iir`) bootstraps Django explicitly
- The project root is required at runtime

This design keeps:
- Django as an internal implementation detail
- The CLI interface simple and stable

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

