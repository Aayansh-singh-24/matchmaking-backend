# Agent Instructions

## Project
- This repository is a Python 3.14+ multiplayer game backend using FastAPI, SQLAlchemy async, Alembic, asyncpg, and MongoDB.
- Application code lives under `src/`; database migrations live under `alembic/`.

## Working guidelines
- Read the relevant source files and existing conventions before making changes.
- Keep changes focused and preserve the current project structure.
- Do not commit secrets, credentials, or local environment files.
- Do not run tests unless the user asks you to test or verify the implementation.
- When changing database models or schema, review whether an Alembic migration is needed.
