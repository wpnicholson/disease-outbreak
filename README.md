# Disease Outbreak Reporting System

## Overview

Develop a web application that allows healthcare professionals to submit and manage disease outbreak reports. This system should demonstrate your expertise in web development, API design, database modelling, and software architecture.

Expected Deliverable: Production-ready code with proper documentation.

## Local Development Instructions

1. Create a Python virtual environment.

    - From the project root, to create a virtual environment named `myvenv` execute the command:

    ```bash
    virtualenv myvenv
    ```

    - Or alternatively:

    ```bash
    python3 -m virtualenv myvenv
    ```

    - Activate the virtual environment on a Windows machine with:

    ```bash
    myvenv/Scripts/Activate
    ```

    - Or, if using a Linux machine:

    ```bash
    source myvenv/bin/activate
    ```

2. Install the development specific Python requirements.

    ```bash
    pip install -r dev-requirements.txt
    ```

3. Copy `.env.example` to `.env` to create your local copy of the required environment variables.

    ```bash
    cp .env.example .env
    ```

    - The Docker setup (see below) will take these values and place them as variables when creating the containers. Therefore you are largely free to define whatever values you want.

4. Beyond the above instructions, you should by and large simply use the Makefile for the majority of your interactions. All commands are to be run from the root directory.

    - For the very first installation, and whenever a full teardown, migration, and rebuild is required, use `make reset-rebuild message="your migration message"`.
    - To seed the database: `make seed`.
    - To test the FastAPI backend api: `make test-cov`.

5. Assuming everything goes according to plan, you can then do the following:

    - Visit `127.0.0.1:8000/docs` to experiment with the FastAPI backend api.
    - Visit `127.0.0.1:5050` and log into pgAdmin, using the credentials `PGADMIN_EMAIL` and `PGADMIN_PASSWORD` as defined in your `.env` file.
      - Inside pgAdmin, right mouse button click on the word "Servers" from the left-hand menu.
      - In the context menu that appears choose "Register" and then "Server".
      - In the popup menu system that appears:
        - On the "General" tab enter `db` into the "Name" field.
        - On the "Connection" tab:
          - Enter `db` into the "Host name/address" field.
          - Enter the value that is set to key `DB_USER` in your `.env` file into the "Username" field.
          - Enter the value that is set to key `DB_PASSWORD` in your `.env` file into the "Password" field.
          - Click the "Save password?" toggle.
        - Click "Save" to exit the popup menu system.
      - You should now notice that when you left mouse click on the word "Servers" from the left-hand menu, this should open up to reveal you database. The database will be named by the value that is set to key `DB_NAME` in your `.env` file.

## Approach

- For the Disease Outbreak Reporting System I will create an application with a FastAPI backend and a SvelteKit frontend. The database will be PostgreSQL.
- I will use a single mono-repo with clearly defined `backend/` and `frontend/` directories.
- I will separate concerns between development and production.
- I will use Docker containers throughout to ensure environment isolation and thus that the application works regardless of the parent operating system. Hence, ensuring standardized operation ready for development, shipment, and deployment.
- I will follow the most professional, mature, and scalable approach for this use case.

## Project Directory Structure

```Bash
disease-outbreak-reporting-system/
│
├── backend/                    # FastAPI app
│   ├── alembic/                # Migration folder
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── README
│   │   └── script.py.mako
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── audit_logs.py  # Audit logging for all data changes.
│   │   │   ├── auth.py
│   │   │   ├── disease.py
│   │   │   ├── export.py
│   │   │   ├── patient.py
│   │   │   ├── reporter.py
│   │   │   ├── reports.py
│   │   │   ├── search.py
│   │   │   └── statistics.py
│   │   ├── __init__.py
│   │   ├── audit_log.py       # Audit logging functionality.
│   │   ├── database.py        # DB engine, SessionLocal, and Base
│   │   ├── dependencies.py    # Proper db session opening and closing.
│   │   ├── enums.py           # enum definitions for Pydantic and SQLAlchemy.
│   │   ├── main.py            # Entry point
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── sample_data.py     # Define sample data and commit to db.
│   │   └── schemas.py         # Pydantic schemas
│   ├── tests/                 # pytest unit/integration tests
│   │   ├── api/
│   │   │   ├── test_audit_logs.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_diseases.py
│   │   │   ├── test_export.py
│   │   │   ├── test_patient.py
│   │   │   ├── test_reporter.py
│   │   │   ├── test_reports.py
│   │   │   ├── test_sample_data.py
│   │   │   ├── test_search.py
│   │   │   └── test_statistics.py
│   │   ├── unit/
│   │   │   ├── test_models.py
│   │   │   ├── test_schemas.py
│   │   │   └── test_utils.py
│   │   └── conftest.py  # Global fixtures for all tests.
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── pytest.ini
│   └── seed_data.py  # Invoke db session to seed database.
│
├── frontend/                  # SvelteKit app
│   ├── src/
│   ├── static/
│   ├── svelte.config.js
│   ├── vite.config.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
│
├── .env                    # Ignored in Docker builds
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .dockerignore
├── .gitignore
├── dev.requirements.txt
├── README.md
└── requirements.txt

```

## Docker Setup

- Docker is used for the backend to ensure compatability across server implementations.
- I also include volumes so that data is persisted even if the containers are shut down.

### `docker-compose.dev.yml`

- This file is located in the root of the project directory structure.
- I define three services:

1. PostgreSQL database.
2. pgAdmin UI.
3. FastAPI backend.

```YML
services:
  db:
    image: postgres:14
    container_name: outbreak_db_container
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U outbreak_db_user -d outbreak_db || exit 0"]
      interval: 5s
      timeout: 5s
      retries: 10

  pgadmin:
    image: dpage/pgadmin4
    container_name: outbreak_pgadmin
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD}
      PGADMIN_CONFIG_SESSION_EXPIRATION_TIME: 43200  # 12 hours
    ports:
      - "5050:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      - db

  backend-app:
    container_name: backend_container
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    working_dir: /code
    volumes:
      - ./backend:/code
    ports:
      - 8000:8000
    env_file:
      - .env
    environment:
      ENV: dev
      DEBUG: "true"
    depends_on:
      db:
        condition: service_healthy
    restart: always

volumes:
  db_data:
  pgadmin_data:
```

### `Dockerfile.dev`

- This file is located in the `backend/` folder of the project directory structure.
- It is called upon as part of the build for the backend FastAPI Docker service.

```Dockerfile
FROM python:3.11-slim

LABEL maintainer="Dr. William Nicholson <williampnicholson@gmail.com>"
LABEL version="0.1.0"
LABEL description="Disease Outbreak Reporting System"

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY dev-requirements.txt .

RUN pip install --upgrade pip && pip install -r dev-requirements.txt

COPY . .

EXPOSE 8000

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "db:5432", "--timeout=60", "--strict", "--", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

```

### `.dockerignore`

- The `.dockerignore` file is located in the project root.

```dockerignore
__pycache__/
*.pyc
.env
tests/
.git
*.md
```

## `.env` within the `backend/` directory

- A `.env` file should be located within the `backend/` directory.
- Since `.env` files should not be shared publicly, a `.env.example` file is provided, which details the structure required from `.env`.

```ENV
# Database configuration.
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_HOST=db
DB_PORT=5432

# SQLAlchemy database URL.
DATABASE_URL=postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

# pgAdmin configuration.
PGADMIN_EMAIL=your_pgadmin_email@example.com
PGADMIN_PASSWORD=your_pgadmin_password

# Database seeding configuration.
JUNIOR_PASSWORD=junior_password
SENIOR_PASSWORD=senior_password

# Environment configuration.
# Set to 'dev' for development, 'prod' for production.
ENV=dev
```

## Alembic setup

- We use Alembic for database migrations.
- Since Alembic is only for backend database migrations it is located within the `backend/` folder.

- Regarding `backend/alembic.ini`, note the following fields and how they should be set:

```alembic.ini
[alembic]
script_location = %(here)s/alembic

sqlalchemy.url =
```

- Why is `sqlalchemy.url =` blank within `backend/alembic.ini`?
  - This value is only read if the `backend/alembic/env.py` loads it from the config directly.
  - But in **modern setups**, we override it in `backend/alembic/env.py` using an environment variable like `DATABASE_URL`, which we establish in `.env`. Thus the real connection string is defined in `.env`.

## Makefile setup

```Makefile
# Makefile for Disease Outbreak Reporting System (Dev Workflow)

DC=docker-compose -f docker-compose.dev.yml
SERVICE=backend-app

## Build all images
build:
  $(DC) build

## Stop and remove all containers, volumes, and orphans
reset:
  $(DC) down --volumes --remove-orphans
  docker system prune -a --volumes -f

## Start all services in the background
up:
  $(DC) up -d
  $(DC) exec $(SERVICE) /wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is ready!"

## Stop all services
down:
  $(DC) down

## Attach to logs
logs:
  $(DC) logs -f $(SERVICE)

## Bash into backend container
bash:
  $(DC) exec $(SERVICE) bash

## Create new Alembic revision (usage: make migrate message="your message")
migrate:
  $(DC) exec $(SERVICE) bash -c "cd /code && alembic revision --autogenerate -m '$(message)'"

## Apply all Alembic migrations
upgrade:
  $(DC) exec $(SERVICE) bash -c "cd /code && alembic upgrade head"

## Create and apply migration in one step (not recommended for production)
quick-migrate:
  $(MAKE) migrate message="$(message)"
  $(MAKE) upgrade

## Wait for database to be ready before starting services
wait-db:
  $(DC) exec $(SERVICE) /wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is up!"

## Reset and rebuild the entire environment, including migrations
reset-rebuild:
  $(MAKE) reset
  $(MAKE) build
  $(MAKE) up
  $(MAKE) upgrade
  $(MAKE) quick-migrate message="$(message)"

## Lint with flake8
lint:
  $(DC) exec $(SERVICE) bash -c "cd /code && flake8 ."

## Format with black
format:
  $(DC) exec $(SERVICE) bash -c "cd /code && black ."

## Run FastAPI server manually (useful for debugging command override)
serve:
  $(DC) exec $(SERVICE) bash -c "cd /code && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

## Run tests (note: inside backend container)
test:
  $(DC) exec $(SERVICE) bash -c "cd /code && pytest tests"

## Run API tests with coverage report (note: inside backend container)
test-cov:
  $(DC) exec $(SERVICE) bash -c "cd /code && pytest --cov=api tests"

## Run API tests with verbose output (note: inside backend container)
test-verbose:
  $(DC) exec $(SERVICE) bash -c "cd /code && pytest -v tests"

## Seed database with sample data
seed:
  $(DC) exec $(SERVICE) bash -c "cd /code && python seed_data.py"
```

## Testing

### To execute testing

- To test the FastAPI backend api, use the Makefile and the command: `make test-cov`.

### Current test coverage

Platform Linux, python 3.11.13-final-0

| Name                        | Stmts | Miss | Cover |
| --------------------------- | ----- | ---- | ----- |
| `api/__init__.py`           | 0     | 0    | 100%  |
| api/audit_log.py            | 7     | 0    | 100%  |
| api/database.py             | 15    | 0    | 100%  |
| api/dependencies.py         | 33    | 5    | 85%   |
| api/endpoints/audit_logs.py | 15    | 0    | 100%  |
| api/endpoints/auth.py       | 43    | 0    | 100%  |
| api/endpoints/disease.py    | 55    | 2    | 96%   |
| api/endpoints/export.py     | 26    | 0    | 100%  |
| api/endpoints/patient.py    | 48    | 0    | 100%  |
| api/endpoints/reporter.py   | 34    | 0    | 100%  |
| api/endpoints/reports.py    | 47    | 0    | 100%  |
| api/endpoints/search.py     | 18    | 0    | 100%  |
| api/endpoints/statistics.py | 19    | 0    | 100%  |
| api/enums.py                | 27    | 0    | 100%  |
| api/main.py                 | 26    | 90   | 65%   |
| api/models.py               | 79    | 1    | 99%   |
| api/sample_data.py          | 39    | 39   | 0%    |
| api/schemas.py              | 109   | 0    | 100%  |

**TOTAL** 640, 56, 91%

| **Column** | **Meaning**                                                                |
| ---------- | -------------------------------------------------------------------------- |
| **Stmts**  | Total number of executable statements (lines of code) in each file.        |
| **Miss**   | Number of statements **not executed by any test** (i.e., missed coverage). |
| **Cover**  | Percentage of statements **executed by your tests** (coverage %).          |

## Endpoint Design

### Available endpoints

- Python files within the `backend/api/endpoints/` folder use FastAPI to define the following endpoints:
  - See the file `reports.py` for the following 7 endpoints:
    - POST /api/reports # Create new report.
    - GET /api/reports # List reports (paginated).
    - GET /api/reports/{id} # Get specific report.
    - PUT /api/reports/{id} # Update report (draft only).
    - DELETE /api/reports/{id} # Delete report (draft only).
    - POST /api/reports/{id}/submit # Submit report (change status).
    - GET /api/reports/recent # Recent submissions.

  - See the file reporter.py for the following 2 endpoints:
    - POST /api/reports/{id}/reporter # Add/update reporter details.
    - GET /api/reports/{id}/reporter # Get reporter details.

  - See the file `patient.py` for the following 2 endpoints:
    - POST /api/reports/{id}/patient # Add/update patient details.
    - GET /api/reports/{id}/patient # Get patient details.

  - See the file `disease.py` for the following 3 endpoints:
    - POST /api/reports/{id}/disease # Add/update disease details.
    - GET /api/reports/{id}/disease # Get disease details.
    - GET /api/diseases/categories # Get disease categories.

  - See the file `search.py` for the following endpoint:
    - GET /api/reports/search # Search reports.

  - See the file `statistics.py` for the following endpoint:
    - GET /api/statistics # Basic statistics.

  - See the file `export.py` for the following endpoint:
    - GET /api/reports/export/{format} # Export data (CSV/JSON).

### Use of FastAPI `APIRouter` class

- Notice that all the endpoints make use of the FastAPI `APIRouter` class. This allows me to group related endpoints, ensure modular code organisation, introduce `tags` for documentation, and use a `prefix` argument for prepending path segments.
- Use of the FastAPI `APIRouter` class also means my main FastAPI application, which is coded within `backend/api/main.py`, is more focussed in it's design and easier to reason.

### Use of enums in endpoint, model, and schema designs

- Also notice that I place all enums into their own Python file, named `backend/api/enums.py`, because enum values are required for both Pydantic type checking and SQLAlchemy type-safe database columns.

#### SQLAlchemy Usage (Database Layer)

- In `backend/api/models.py`, the enums are used within **SQLAlchemy ORM models**.
- For example:

```python
from sqlalchemy import Enum as SqlEnum
from api.enums import DiseaseCategoryEnum

disease_category: Mapped[DiseaseCategoryEnum] = mapped_column(
    SqlEnum(DiseaseCategoryEnum), nullable=False
)
```

- SQLAlchemy’s `SqlEnum()` converts a Python `Enum` value into a database column using **PostgreSQL’s ENUM type** or a text type depending on backend.
- Benefit: I get type-safe database columns that only accept valid enum values.

#### Pydantic Usage (Validation Layer)

- In `backend/api/schemas.py`, the enums are used for **request validation** and **response serialization**.
- For example:

```python
from api.enums import DiseaseCategoryEnum
from pydantic import BaseModel

class DiseaseBase(BaseModel):
    disease_category: DiseaseCategoryEnum
```

- Pydantic will:
  - Validate input to only accept allowed enum values (`Bacterial`, `Viral`, `Parasitic`, `Other`).
  - Serialize responses showing the enum **value** (string) rather than the Python object.

#### Enum summary

| **Layer**      | **Usage**                               | **Effect**                                                   |
| -------------- | --------------------------------------- | ------------------------------------------------------------ |
| **SQLAlchemy** | `SqlEnum(DiseaseCategoryEnum)`          | Database-level enforcement of enum constraints               |
| **Pydantic**   | `disease_category: DiseaseCategoryEnum` | Automatic validation & serialization/deserialization of data |

- By defining enums once in `backend/api/enums.py`, we achieve **single source of truth** for business logic and **consistency across your entire application stack** - from **API validation** to **database schema**.

## User authentication system

- The frontend allows users to create an account and log into that account.
- Therefore `User` table has been created in `backend/api/models.py`.
- This effects the three audit fields (`created_at`, `updated_at`, `created_by`) within the SQLAlchemy declarative base model `class Report(Base)` (also within `backend/api/models.py`).
  - The `created_by` field within `Report` model is a foreign key to the `User` model.

## Original Challenge Description

### Technical Requirements

#### Framework & Technology Stack

- Backend: FastAPI, Flask, or Django.
- Database: PostgreSQL (preferred) or SQLite for development.
- ORM: SQLAlchemy (FastAPI/Flask) or Django ORM.
- API Documentation: OpenAPI/Swagger integration.
- Testing: pytest or unittest with meaningful test coverage.
- Configuration: Environment variables for all settings.

#### Core Architecture Requirements

- Follow MVC/MVT pattern.
- Implement proper separation of concerns.
- Use dependency injection where appropriate.
- Include comprehensive error handling.
- Implement audit logging for all data changes.

### Application Features

#### 1. Reporter Details Page

- Fields:
  - First name (required, max 50 chars).
  - Last name (required, max 50 chars).
  - Email (required, unique, valid email format).
  - Job title (required, max 100 chars).
  - Phone number (required, format validation).
  - Hospital/Organization name (required, max 200 chars).

- Hospital address (required, max 500 chars)
  - Registration date (auto-populated).

#### 2. Patient Details Page

- Fields:
  - First name (required, max 50 chars).
  - Last name (required, max 50 chars).
  - Date of birth (required, no future dates).
  - Age (calculated field, display only).
  - Gender (required, enum: Male/Female/Other).
  - Medical record number (required, unique per hospital).
  - Patient address (required, max 500 chars).
  - Emergency contact (optional, max 200 chars).

#### 3. Disease Details Page

- Fields:
  - Disease name (required, max 100 chars).
  - Disease category (required, enum: Bacterial/Viral/Parasitic/Other).
  - Date detected (required, cannot be future date, cannot be before patient DOB).
  - Symptoms (required, JSON array or text field).
  - Severity level (required, enum: Low/Medium/High/Critical).
  - Lab results (optional, text field).
  - Treatment status (required, enum: None/Ongoing/Completed).

#### 4. Summary Page

- Display all entered information in read-only format.
- Show validation status for each section.
- Include links to edit each section (if report status is 'draft').
- Display report metadata (created date, last modified, status).
- Submit button to finalize report.
- Clear visual indication of required vs optional fields.

### API Requirements

#### Core CRUD Endpoints

- `POST` `/api/reports # Create new report`
- `GET` `/api/reports # List reports (paginated)`
- `GET` `/api/reports/{id} # Get specific report`
- `PUT` `/api/reports/{id} # Update report (draft only)`
- `DELETE` `/api/reports/{id} # Delete report (draft only)`
- `POST` `/api/reports/{id}/reporter # Add/update reporter details`
- `GET` `/api/reports/{id}/reporter # Get reporter details`
- `POST` `/api/reports/{id}/patient # Add/update patient details`
- `GET` `/api/reports/{id}/patient # Get patient details`
- `POST` `/api/reports/{id}/disease # Add/update disease details`
- `GET` `/api/reports/{id}/disease # Get disease details`
- `POST` `/api/reports/{id}/submit # Submit report (change status)`
- `GET` `/api/reports/search # Search reports`
- `GET` `/api/statistics # Basic statistics`

#### Advanced Endpoints

- `GET` `/api/reports/export/{format} # Export data (CSV/JSON)`
- `GET` `/api/diseases/categories # Get disease categories`
- `GET` `/api/reports/recent # Recent submissions`

### Data Model Requirements

#### Database Design

- Implement proper foreign key relationships.
- Use appropriate data types and constraints.
- Add database indexes for performance.
- Include audit fields (`created_at`, `updated_at`, `created_by`).

#### Report States

- Draft: Editable, incomplete reports.
- Submitted: Complete, read-only reports.
- Under Review: Being reviewed by editor (optional feature).
- Approved: Final approved reports.

#### Validation Rules

- Cross-field validation (disease date vs patient DOB).
- Email uniqueness per reporter.
- Medical record number uniqueness per hospital.
- Date range validations.
- Required field enforcement.
- Data type validation.

### Security & Performance

#### Security Requirements

- Input sanitization for all user inputs.
- SQL injection prevention.
- CSRF protection (for web forms).
- Rate limiting on API endpoints.
- Secure session management.
- Environment-based configuration.

#### Performance Requirements

- Implement pagination (20 items per page).
- Add database indexing strategy.
- Optimize queries to prevent N+1 problems.
- Include basic caching for reference data.
- Handle concurrent access appropriately.

### Testing Requirements

#### Test Coverage Expected

- Unit tests for business logic (minimum 80% coverage).
- Integration tests for API endpoints.
- Database model tests.
- Validation logic tests.
- Error handling tests.

#### Test Scenarios

- Valid data submission flow.
- Invalid data rejection.
- State transition validation.
- Concurrent access scenarios.
- Edge cases and error conditions.

### Optional Advanced Features (Bonus Points)

#### User Management System

- Editor Role: Can review, edit, and prioritize submitted reports.
- Reporter Role: Can only create and edit their own draft reports.
- Admin Role: Full system access and user management.

#### Advanced Features

- Real-time notifications for new submissions.
- Geographic mapping of outbreak locations.
- Data export functionality (CSV, PDF reports).
- Dashboard with analytics and charts.
- Integration with external disease databases.
- Docker containerization with docker-compose.

### Evaluation Criteria

#### Code Architecture & Design (30%)

- Clean, maintainable code structure.
- Proper separation of concerns.
- Design patterns usage.
- Database schema design.

#### API Design & Implementation (25%)

- RESTful API principles.
- Proper HTTP status codes.
- Comprehensive error handling.
- API documentation quality.

#### Data Validation & Security (20%)

- Input validation implementation.
- Security best practices.
- Error message handling.
- Data integrity maintenance.

#### Testing & Documentation (15%)

- Test coverage and quality.
- README documentation.
- Code comments and docstrings.
- Setup instructions.

#### Performance & Scalability (10%)

- Database optimization.
- Query ebiciency.
- Caching strategy.
- Resource usage.

### Submission Requirements

#### Deliverables

1. Source Code: Complete application with all features.
2. README.md: Setup instructions, API documentation, architecture overview.
3. Tests: Comprehensive test suite with instructions to run.
4. Database: Schema migration files or setup scripts.
5. Requirements: dependencies file (`requirements.txt` or `pyproject.toml`).
6. Configuration: Environment variable documentation.

#### Setup Instructions

- Setup instructions should include the following:
  - Virtual environment setup.
  - Database setup and migrations.
  - Environment variable configuration.
  - How to run the application.
  - How to run tests.
  - API endpoint documentation.

### Discussion Points (Post-Implementation)

- Be prepared to discuss the following:
  - How would you scale this system for 10,000+ concurrent users?
  - What monitoring and logging would you implement in production?
  - How would you handle HIPAA compliance and data privacy?
  - Database backup and disaster recovery strategy.
  - Performance optimization strategies.
  - Security audit considerations.

### Sample Data

- Include fixtures or sample data for the following:
  - 3-5 sample reporters.
  - 10-15 sample patients.
  - Various disease types and severity levels.
  - Reports in different states (draft, submitted, approved).
