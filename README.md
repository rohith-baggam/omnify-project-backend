This repository contains the backend service for the **Omnify** project, a structured Django REST API application. The codebase is built with clean architecture principles and includes pre-commit hooks for code quality, a Dockerized PostgreSQL setup, and complete API documentation via Postman.

## 📂 Project Structure

- `project_utils/` – Contains utility scripts and resources.
- `Docker/` – Docker container configurations for local development.
- `docs/` – Includes DBML scripts and PDF exports of the database schema.
- `postman/` – JSON exports and links to live Postman API docs.
- `coreutils/` – Custom pre-commit hooks and validation scripts.

---

## 🗄️ Database Architecture

You can explore the full database schema using the following resource:

🔗 **DB Diagram**: [View on dbdocs.io](https://dbdocs.io/rohithrajbaggam/Omnify) (https://dbdocs.io/rohithrajbaggam/Omnify)

---

## 🚀 Getting Started

### 📦 Requirements

Ensure the following Python packages are installed (managed via `requirements.txt`):

```
cryptography==45.0.4
Django==5.2.3
django-cors-headers==4.7.0
django-filter==25.1
django-user-agents==0.4.0
djangorestframework==3.16.0
drf-jwt==1.19.2
drf-yasg==1.21.10
filelock==3.18.0
identify==2.6.12
inflection==0.5.1
nodeenv==1.9.1
packaging==25.0
platformdirs==4.3.8
pre_commit==4.2.0
psycopg2-binary==2.9.10
pycparser==2.22
PyJWT==2.10.1
python-decouple==3.8
pytz==2025.2
PyYAML==6.0.2
user-agents==2.2.0
virtualenv==20.31.2
```

### 🐳 Database Setup (Docker)

Start the PostgreSQL database using Docker Compose:

```yaml
version: "3.9"
services:
  aptagrim_postgres_database:
    image: postgres
    restart: always
    environment:
      - POSTGRES_DB=TEST_POSTGRES
      - POSTGRES_USER=test
      - POSTGRES_PASSWORD=Abcd.1234
    ports:
      - "9051:5432"
```

**Django DB Configuration:**

```python
DB_NAME = "TEST_POSTGRES"
DB_USER = "test"
DB_PASSWORD = "Abcd.1234"
DB_HOST = "localhost"
DB_PORT = "9051"
ENGINE = 'django.db.backends.postgresql'
```

---

## 📑 API Documentation

🧾 **Live Postman Collection**:

https://documenter.getpostman.com/view/28644884/2sB2xBEqhX

You can also import the Postman JSON file from the `postman/` directory to test the endpoints locally.

---

## 🧰 Development & Code Quality

The project uses [**pre-commit**](https://pre-commit.com/) for enforcing consistent code quality. Hooks include:

- ✅ YAML and whitespace checks
- 🧪 Python code formatting via **Black**
- 🔍 Custom checks for variable naming and duplicate classes

### Setup Pre-commit

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Sample `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-docstring-first

  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black
        language_version: python3.12

  - repo: local
    hooks:
      - id: check-variable-naming
        name: Check variable naming
        entry: python coreutils/utils/pre_commit/precommit_check_variable_naming.py
        language: python
        pass_filenames: true

  - repo: local
    hooks:
      - id: check-duplicate-classes
        name: Delete Empty Python Files
        entry: python coreutils/utils/pre_commit/check_duplicate_class_names.py
        language: system
        types: [python]
```
