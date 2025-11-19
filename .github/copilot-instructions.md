<!--
Purpose: short, actionable guidance to help AI coding agents be productive in this repo.
Keep concise and reference concrete files/commands discovered in the workspace.
-->
# Copilot instructions for TeamPy (team-teampy)

This repository is a small Flask application (blueprint-based) used for a class project. Below are the key patterns, workflows, and examples an AI agent should follow when making or proposing changes.

## Big picture
- **App type:** Flask app created by `create_app` in `app/__init__.py` and configured with `Config` from `config.py`.
- **Blueprints:** Four main blueprints registered in `create_app`: `faculty`, `student`, `auth`, and `errors`. Each blueprint lives under `app/<name>/` and defines a `<name>_blueprint` in its `__init__.py` (e.g. `app/faculty/__init__.py`).
- **Templates & static:** Templates are stored in `app/*/templates` but `create_app` sets template folder locations using constants in `config.py` (e.g. `TEMPLATE_FOLDER_FACULTY`) and assigns them to each blueprint before registering. Static files are under `app/static` and referenced via `STATIC_FOLDER` in `config.py`.
- **Data layer:** SQLAlchemy via the `db` object from `app/__init__.py`. Models live in `app/*/*_models.py` and forms in `app/*/*_forms.py`.
- **Other services:** Flask-Mail is configured in `config.py` using environment variables; an `app.serializer` (URLSafeTimedSerializer) is created for token generation.

## How to run & common dev commands
- Run locally (development): `python research.py` (this file creates the app with `Config` and runs `app.run(debug=True)`).
- Flask CLI (migrations & shell): set `FLASK_APP` to `research.py`. In PowerShell:
  - `$env:FLASK_APP = 'research.py'`
  - `$env:FLASK_ENV = 'development'`
  - Then use `flask run` or `flask db migrate` / `flask db upgrade` for migrations.
- Tests: run `pytest -q` from repo root. Tests create an app via `create_app` with a `TestConfig` that uses an in-memory sqlite DB.
- Docker: the repo includes `build.sh` with docker commands; on Windows run the script via WSL/bash or run the same commands directly in PowerShell.

## Environment & configuration
- This project uses `python-dotenv`. Put local secrets in a `.env` at repo root. `config.py` reads:
  - `SECRET_KEY`, `DATABASE_URL`, `MAIL_USERNAME`, `MAIL_PASSWORD`.
- Defaults: if `DATABASE_URL` is not set, the app falls back to an sqlite file `smile.db` in the repo root.

## Code patterns and conventions (important for edits)
- File naming: routes in `*_routes.py`, models in `*_models.py`, forms in `*_forms.py`.
- Blueprint variables: each package exposes `<name>_blueprint` in its `__init__.py`. Use those when importing (e.g. `from app.faculty import faculty_blueprint as faculty`).
- Template assignment: `create_app` sets `blueprint.template_folder = Config.TEMPLATE_FOLDER_*` before `app.register_blueprint(...)`. Do not duplicate template folder logic in blueprints — rely on `create_app` behavior.
- DB usage: import `db` from `app` and use `db.session.add(...)`, `db.session.commit()` or `db.create_all()` as shown in `research.py` and route handlers.
- Login and authorization: uses `flask_login`. Routes that require users use `@login_required`. User object fields (like `.is_faculty`) determine role checks (see `faculty_routes.py`). Use `abort(403)` for unauthorized access.
- Form patterns: Many-to-many selections are implemented by querying models with `.id.in_(form.field.data)` and then extending or replacing relationship lists (see `app/faculty/faculty_routes.py` `create_position` and `edit_position`). Use the same approach when updating relationships.

## Examples (copy these patterns when editing or adding features)
- Registering a blueprint and template folder (from `app/__init__.py`):
  - `from app.faculty import faculty_blueprint as faculty`
  - `faculty.template_folder = Config.TEMPLATE_FOLDER_FACULTY`
  - `app.register_blueprint(faculty)`
- Query many-to-many selections (from `app/faculty/faculty_routes.py`):
  - `selected_majors = Major.query.filter(Major.id.in_(form.majors.data)).all()`
  - `position.majors.extend(selected_majors)` and later `db.session.commit()`.

## Tests & CI expectations
- Unit/functional tests use `pytest`. Tests construct the app via `create_app(TestConfig)` and rely on `WTF_CSRF_ENABLED = False` in `TestConfig` for form posts.
- When modifying endpoints that tests touch (`/user/register`, `/user/login`, `/post`, etc.), run the relevant tests to ensure responses and DB updates still match expected assertions.

## Integration points & external services
- Email: configured to use Gmail SMTP in `config.py`. Real credentials must be placed in `.env` (`MAIL_USERNAME`, `MAIL_PASSWORD`).
- Docker Hub: `build.sh` tags and pushes `arslanay/softengdemo` — update this if you change docker repo names.

## Repo issues I noticed (be cautious)
- There are merge conflict markers in `app/faculty/faculty_routes.py`. Resolve merge markers before making substantial changes that touch that file.

## Guidance for AI edits (do this first when proposing changes)
1. Read `app/__init__.py` and `config.py` to ensure blueprint/template assumptions are preserved.
2. Match existing naming and import patterns (`from app import db`, use `@bp.route` with the blueprint object from the package `__init__.py`).
3. When adding DB-backed features, prefer migration (Flask-Migrate) over `db.create_all()` in production code. Use `flask db migrate` / `flask db upgrade` for schema changes.
4. Run `pytest` locally after changes; tests expect in-memory sqlite behavior.
5. If your patch modifies templates, update the matching `TEMPLATE_FOLDER_*` only in `config.py` or via the blueprint assignment in `create_app` — do not scatter absolute template paths.

If anything here is unclear or you want me to expand sections (examples, common refactor patterns, or a brief mapping of models → routes), tell me which area to expand.
