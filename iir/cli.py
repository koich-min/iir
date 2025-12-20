import os
import sys
from importlib import metadata
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SECRET_PATH = PROJECT_ROOT / ".env.secret"

COMMAND_MAP = {
    "replace": "replace_text",
    "add-entry": "add_entry",
}
AVAILABLE_SUBCOMMANDS = sorted([*COMMAND_MAP, "dev-init", "version"])


def main(argv=None):
    argv = list(argv) if argv is not None else sys.argv[1:]

    if not argv:
        sys.stderr.write(_usage())
        return 1

    subcommand, *rest = argv
    if subcommand == "--help":
        # Treat top-level help as a successful invocation (no Django init).
        sys.stdout.write(_usage())
        return 0
    if subcommand == "--version":
        print(f"iir {metadata.version('iir')}")
        return 0
    if subcommand == "version":
        print(f"iir {metadata.version('iir')}")
        return 0
    if subcommand == "dev-init":
        return dev_init()

    command = COMMAND_MAP.get(subcommand)
    if command is None:
        sys.stderr.write(f"Unknown subcommand: {subcommand}\n")
        sys.stderr.write(_usage())
        return 1

    # ★ 追加：Django プロジェクトルートを import path に追加
    sys.path.insert(0, str(PROJECT_ROOT))

    import django
    from django.core.management import call_command

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "svr.settings")
    django.setup()

    call_command(command, *rest)
    return 0


def dev_init():
    from django.core.management.utils import get_random_secret_key

    if SECRET_PATH.exists():
        print(".env.secret already exists, nothing to do")
        return 0

    secret = get_random_secret_key()
    SECRET_PATH.write_text(f"DJANGO_SECRET_KEY=\"{secret}\"\n")
    print("Created .env.secret with DJANGO_SECRET_KEY")
    return 0


def _usage():
    available = ", ".join(AVAILABLE_SUBCOMMANDS)
    return (
        "Usage: iir <subcommand> [options]\n"
        f"Subcommands: {available}\n"
    )


if __name__ == "__main__":  # pragma: no cover - manual execution guard
    sys.exit(main())
