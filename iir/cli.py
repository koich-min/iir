import os
import sys
from pathlib import Path
import django
from django.core.management import call_command


COMMAND_MAP = {
    "replace": "replace_text",
    "add-entry": "add_entry",
}


def main(argv=None):
    argv = list(argv) if argv is not None else sys.argv[1:]

    if not argv:
        sys.stderr.write(_usage())
        return 1

    subcommand, *rest = argv
    command = COMMAND_MAP.get(subcommand)
    if command is None:
        sys.stderr.write(f"Unknown subcommand: {subcommand}\n")
        sys.stderr.write(_usage())
        return 1

    # ★ 追加：Django プロジェクトルートを import path に追加
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "svr.settings")
    django.setup()

    call_command(command, *rest)
    return 0


def _usage():
    available = ", ".join(sorted(COMMAND_MAP))
    return (
        "Usage: iir <subcommand> [options]\n"
        f"Subcommands: {available}\n"
    )


if __name__ == "__main__":  # pragma: no cover - manual execution guard
    sys.exit(main())
