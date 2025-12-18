# Initial Administrative Setup (Kubernetes)

This document describes manual administrative setup steps to be performed after deploying iir on Kubernetes.

These steps are intentionally not automated.

iir assumes that:
- humans make mistakes
- administrative actions must be explicit
- secrets should not be embedded in manifests or images

---

## Prerequisites

- iir Deployment is running
- Database migrations have completed
- You have kubectl access to the cluster
- You understand that these actions affect production data

---

## 1. Creating the Initial Django Superuser

iir does not create admin users automatically.

To create the initial Django superuser, execute the following command against a running iir Pod.

### Step 1: Identify a running Pod

cubectl get pods -n home

Example:

iir-6c7f8c9d7b-abcde

---

### Step 2: Run createsuperuser interactively

cubectl exec -n home -it iir-6c7f8c9d7b-abcde-- python manage.py createsuperuser

You will be prompted for:

- Username
- Email address
- Password

This operation writes directly to the shared database.
Running it on any one Pod is sufficient.

---

### Notes

- This command is interactive by design
- Passwords are never stored in manifests or logs
- The Pod is not modified
- No Kubernetes resources are created

---

## 2. Accessing the Django Admin Site

After creating a superuser, access the admin site:

https://<your-hostname>/admin/

Use the credentials created in the previous step.

The admin interface is intended for:
- dictionary management
- internal inspection
- limited administrative tasks

---

## 3. Issuing API Tokens (if required)

If API authentication is enabled and tokens are required,
they should be issued manually by an administrator.

This is typically done via:
- Django admin interface
- or Django shell via kubectl exec

### Example: Enter Django shell

kubectl exec -n home -it iir-xxxxxxxxxx-yyyyy -- python manage.py shell

From there, tokens can be created according to the
authentication mechanism in use.

 (Exact commands depend on the chosen auth backend.)

---

## Why exec-based administration is used

iir intentionally favors kubectl exec for initial administration:

- No secrets embedded in YAML
- No one-shot Jobs left behind
- Clear operator intent
- Aligns with the project's safety philosophy

Convenience is traded for clarity and safety.

---

## What is intentionally *not* automated

The following actions are not automated by design:

- Superuser creation
- API token issuance
- Dictionary bootstrap data
- Privilege escalation

Ese operations define trust boundaries and must remain explicit.

---

## Summary

- Initial admin setup is performed manually
- kubectl exec is the recommended mechanism
- No credentials are stored in manifests
- Actions are auditable and deliberate

This keeps iir safe even when humans forget things.
