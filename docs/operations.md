# Operations Guide (Advanced)

This document describes **advanced and low-level operational tasks** for iir.

It is intended for **developers and operators** who are responsible for
environment bootstrap, data migration, backup, or recovery.

⚠️ **This document intentionally covers operations that are *not* exposed via the iir CLI.**

If you are a general user, you typically do **not** need this document.
Day-to-day operation should be performed via:

- CLI (`iir add-entry`, `iir replace`)
- Administrative CLI (`iir admin`, `iir api`)
- Management Console (Django Admin)

---

## Positioning and Responsibility

This document exists to describe **bulk, destructive, or exceptional operations**
that are intentionally kept **outside** the normal CLI surface.

### What belongs here

- Bulk data export or import
- Full dictionary backup and restore
- Environment bootstrap or recovery
- Controlled testing of deployment procedures

### What does *not* belong here

If an operation can be performed via:

- `iir add-entry`
- `iir replace`
- `iir admin`
- `iir api`

it does **not** belong in this document.

Those operations are covered by:

- `docs/quickstart.md`
- `docs/maintenance.md`

---

## Scope and Warnings

The operations described here:

- Operate on the dictionary database directly
- May affect **all entries at once**
- Are not reversible automatically

⚠️ **These commands should only be used by operators who understand the impact.**

For normal usage, always prefer:

- CLI (`iir add-entry`)
- Management Console

---

## When This Document Is Useful

Typical scenarios include:

- Bootstrapping a new environment
- Migrating dictionary data between environments
- Creating a controlled backup
- Restoring data after accidental deletion
- Testing deployment or recovery procedures

---

## Backup (Exporting Dictionary Data)

iir stores its dictionary using Django models.  
For backup purposes, Django provides a built-in export mechanism.

This creates a **structured snapshot** of the dictionary data.

Example (run inside the container, pod, or a controlled environment):

```sh
python manage.py dumpdata dictionary --indent 2 > dictionary.json
```

This command:

- Exports all dictionary-related data
- Preserves categories, IDs, and relationships
- Produces a human-readable JSON file

Store the resulting file securely.

---

## Restore (Importing Dictionary Data)

To restore dictionary data from a backup file:

```sh
python manage.py loaddata dictionary.json
```

Important notes:

- Existing entries may be overwritten
- IDs are restored as-is
- This is a bulk operation

⚠️ Always verify the target environment before restoring.

---

## Operational Recommendations

- Perform backup and restore operations during maintenance windows
- Avoid running these commands automatically
- Do not expose these operations via API or UI
- Treat backup files as sensitive internal assets

---

## Relationship to Other Usage Modes

### Local / Personal Mode

Useful for experimentation and testing.

### Container / Shared Mode

Backup and restore should be performed manually by operators only.

These operations are intentionally **not part of the normal application flow**.

---

## Design Rationale

iir prioritizes structural safety.

Bulk operations such as backup and restore are powerful but dangerous.
For this reason:

- They are not part of the public API
- They are not exposed to general users
- They require explicit operator intent

This reduces the risk of accidental large-scale changes.

---

## Summary

- Backup and restore are supported via Django’s standard tools
- These operations are intended for developers and operators only
- Day-to-day dictionary management should use explicit, incremental methods

If you are unsure whether you need these commands, you probably do not.

