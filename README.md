# iir — Internal Info Replacement

iir (Internal Info Replacement) is a lightweight system for safely replacing
internal identifiers (hosts, domains, service names, etc.) before sharing logs,
documents, or prompts with external parties or AI systems.

The core idea is simple:

- Maintain an explicit dictionary of internal identifiers
- Replace them deterministically with pseudonyms
- Never leak internal naming conventions outside

---

## Key Features

- Deterministic pseudonymization based on dictionary entries
- Exact-match replacement (no fuzzy or partial matching)
- Categories are free-form and user-defined
- Web-based replace form (Django)
- CLI-friendly bulk registration via stdin
- Designed to work with existing UNIX tools

---

## Core Concepts

### Entry

An Entry represents one internal identifier.

- category: logical label (e.g. HOST, DOMAIN, SERVICE, WORD)
- value: the exact string to replace
- is_active: whether the entry participates in replacement

Categories are **labels only**.
They are not constrained or enforced by the system.

---

### Replacement Rules

- Only exact string matches are replaced
- Active entries only
- Longer values are replaced first to avoid substring collisions
- Pseudonyms are generated as: `<Category><id>`

Example:

- HOST:srv-prod-01 → Host12

---

## Web Replace Form

The replace form allows you to paste text and replace internal identifiers.

- Categories shown as checkboxes are derived from existing Entry data
- By default, all available categories are selected
- Unchecked categories are ignored during replacement

This form is intended for:
- Preparing logs for external sharing
- Sanitizing text before sending to AI tools
- Manual inspection and validation

---

## Registering Entries (CLI)

iir is designed to integrate with existing system tools.
Entries are registered explicitly via a Django management command.

### add_entry command

Reads values line-by-line from stdin and registers them as Entry records.

Usage:

    python manage.py add_entry <CATEGORY>

Example:

    echo srv-prod-01 | python manage.py add_entry HOST

Duplicate entries are ignored safely.

---

### Example: Import domain from echo

```bash
echo "my.domain" | pipenv run python manage.py add_entry DOMAIN
```


### Example: Import hosts from DNS (AXFR)

If your internal DNS allows zone transfer:

    dig axfr my.domain @dns-server \
      | awk '{print $1}' \
      | sed 's/\\.$//' \
      | sort -u \
      | python manage.py add_entry HOST

Notes:
- Only names are imported (IPs are ignored)
- Trailing dots from FQDNs are removed safely
- Review entries in Django admin if needed

---

## Design Philosophy

- iir does not auto-discover internal identifiers
- All entries are explicit and human-curated
- Existing UNIX tools are preferred over custom scanners
- Replacement accuracy is prioritized over coverage

This keeps the dictionary trustworthy and predictable.

---

## Security Considerations

- Replacement rules are never exposed externally
- Pseudonyms are deterministic but non-reversible without the database
- No original identifiers appear in output
- Designed as a safety layer before external sharing or AI usage

---

## Development

- Framework: Django
- Database-backed dictionary
- Intended for containerized / k8s environments
- Minimal dependencies

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

