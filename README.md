# TeamPy Research Portal

## Description
A Flask-based research opportunity portal that connects faculty and students. Faculty can create and manage research positions, and students can browse, apply, and manage applications. The system uses SQLAlchemy for data modeling, Flask-Login for authentication, and Flask-Mail for verification workflows.

## Installation
1) Create and activate a virtual environment:
	- Windows PowerShell:
	  ```powershell
	  python -m venv .venv
	  .\.venv\Scripts\Activate.ps1
	  ```

2) Install dependencies:
	```powershell
	pip install -r requirements.txt
	```

3) Configure environment variables in a `.env` file (repo root):
	- `SECRET_KEY`
	- `DATABASE_URL` (optional; defaults to sqlite)
	- `MAIL_USERNAME`
	- `MAIL_PASSWORD`
	- `AUTH0_DOMAIN`
	- `AUTH0_CLIENT_ID`
	- `AUTH0_CLIENT_SECRET`
	- `AUTH0_REDIRECT_URI`

## Usage
Run the app locally:
```powershell
python src/research.py
```

For Flask CLI (migrations, shell):
```powershell
$env:FLASK_APP = 'src/research.py'
$env:FLASK_ENV = 'development'
flask run
```

Run tests:
```powershell
pytest -q
```

## Project Structure
```
.
├─ src/
│  ├─ app/
│  │  ├─ auth/
│  │  ├─ faculty/
│  │  ├─ student/
│  │  ├─ errors/
│  │  ├─ models/
│  │  └─ static/
│  ├─ config.py
│  └─ research.py
├─ tests/
├─ migrations/
├─ docs/
├─ requirements.txt
├─ Dockerfile
└─ README.md
```
