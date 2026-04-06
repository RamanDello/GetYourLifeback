# CLAUDE.md

## Project

Django app (cookiecutter-django) using Docker Compose for local dev with a VS Code devcontainer.

## Dev Environment Setup

1. Make sure **Docker Desktop** is running before opening VS Code
2. Open the project folder in VS Code
3. `Ctrl+Shift+P` -> "Dev Containers: Reopen in Container"
4. App runs at http://localhost:8000

### Troubleshooting

- **"docker command not found"**: Fully quit VS Code (including system tray), ensure Docker Desktop is running, then reopen VS Code. VS Code loads PATH at startup.
- **Python interpreter warning**: Dismiss it. The devcontainer.json sets the correct container Python path (`/usr/local/bin/python`). The warning is about the local Windows Python which is irrelevant inside the container.

## Stack

- Python 3.14 / Django 6 / PostgreSQL 18
- Package manager: uv (lockfile: uv.lock)
- Formatter/linter: ruff
- Settings: `config/settings/local.py` (local), `config/settings/production.py` (prod)
- Env files: `.envs/.local/.django`, `.envs/.local/.postgres`
