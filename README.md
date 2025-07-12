# Disease Outbreak Reporting System

## Overview

Develop a web application that allows healthcare professionals to submit and manage disease outbreak reports. This system should demonstrate your expertise in web development, API design, database modelling, and software architecture.

Expected Deliverable: Production-ready code with proper documentation.

## Environment Variables

1. Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

## Local Development Notes

```Bash
pip install -r dev-requirements.txt
```

## Technical Requirements

### Framework & Technology Stack

- Backend: FastAPI, Flask, or Django.
- Database: PostgreSQL (preferred) or SQLite for development.
- ORM: SQLAlchemy (FastAPI/Flask) or Django ORM.
- API Documentation: OpenAPI/Swagger integration.
- Testing: pytest or unittest with meaningful test coverage.
- Configuration: Environment variables for all settings.

### Core Architecture Requirements

- Follow MVC/MVT pattern.
- Implement proper separation of concerns.
- Use dependency injection where appropriate.
- Include comprehensive error handling.
- Implement audit logging for all data changes.

## Application Features

### 1. Reporter Details Page

- Fields:
  - First name (required, max 50 chars).
  - Last name (required, max 50 chars).
  - Email (required, unique, valid email format).
  - Job title (required, max 100 chars).
  - Phone number (required, format validation).
  - Hospital/Organization name (required, max 200 chars).

- Hospital address (required, max 500 chars)
  - Registration date (auto-populated).

### 2. Patient Details Page

- Fields:
  - First name (required, max 50 chars).
  - Last name (required, max 50 chars).
  - Date of birth (required, no future dates).
  - Age (calculated field, display only).
  - Gender (required, enum: Male/Female/Other).
  - Medical record number (required, unique per hospital).
  - Patient address (required, max 500 chars).
  - Emergency contact (optional, max 200 chars).

### 3. Disease Details Page

- Fields:
  - Disease name (required, max 100 chars).
  - Disease category (required, enum: Bacterial/Viral/Parasitic/Other).
  - Date detected (required, cannot be future date, cannot be before patient DOB).
  - Symptoms (required, JSON array or text field).
  - Severity level (required, enum: Low/Medium/High/Critical).
  - Lab results (optional, text field).
  - Treatment status (required, enum: None/Ongoing/Completed).

### 4. Summary Page

- Display all entered information in read-only format.
- Show validation status for each section.
- Include links to edit each section (if report status is 'draft').
- Display report metadata (created date, last modified, status).
- Submit button to finalize report.
- Clear visual indication of required vs optional fields.

## API Requirements

### Core CRUD Endpoints

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

### Advanced Endpoints

- `GET` `/api/reports/export/{format} # Export data (CSV/JSON)`
- `GET` `/api/diseases/categories # Get disease categories`
- `GET` `/api/reports/recent # Recent submissions`

## Data Model Requirements

### Database Design

- Implement proper foreign key relationships.
- Use appropriate data types and constraints.
- Add database indexes for performance.
- Include audit fields (`created_at`, `updated_at`, `created_by`).

### Report States

- Draft: Editable, incomplete reports.
- Submitted: Complete, read-only reports.
- Under Review: Being reviewed by editor (optional feature).
- Approved: Final approved reports.

### Validation Rules

- Cross-field validation (disease date vs patient DOB).
- Email uniqueness per reporter.
- Medical record number uniqueness per hospital.
- Date range validations.
- Required field enforcement.
- Data type validation.

## Security & Performance

### Security Requirements

- Input sanitization for all user inputs.
- SQL injection prevention.
- CSRF protection (for web forms).
- Rate limiting on API endpoints.
- Secure session management.
- Environment-based configuration.

### Performance Requirements

- Implement pagination (20 items per page).
- Add database indexing strategy.
- Optimize queries to prevent N+1 problems.
- Include basic caching for reference data.
- Handle concurrent access appropriately.

## Testing Requirements

### Test Coverage Expected

- Unit tests for business logic (minimum 80% coverage).
- Integration tests for API endpoints.
- Database model tests.
- Validation logic tests.
- Error handling tests.

### Test Scenarios

- Valid data submission flow.
- Invalid data rejection.
- State transition validation.
- Concurrent access scenarios.
- Edge cases and error conditions.

## Optional Advanced Features (Bonus Points)

### User Management System

- Editor Role: Can review, edit, and prioritize submitted reports.
- Reporter Role: Can only create and edit their own draft reports.
- Admin Role: Full system access and user management.

### Advanced Features

- Real-time notifications for new submissions.
- Geographic mapping of outbreak locations.
- Data export functionality (CSV, PDF reports).
- Dashboard with analytics and charts.
- Integration with external disease databases.
- Docker containerization with docker-compose.

## Evaluation Criteria

### Code Architecture & Design (30%)

- Clean, maintainable code structure.
- Proper separation of concerns.
- Design patterns usage.
- Database schema design.

### API Design & Implementation (25%)

- RESTful API principles.
- Proper HTTP status codes.
- Comprehensive error handling.
- API documentation quality.

### Data Validation & Security (20%)

- Input validation implementation.
- Security best practices.
- Error message handling.
- Data integrity maintenance.

### Testing & Documentation (15%)

- Test coverage and quality.
- README documentation.
- Code comments and docstrings.
- Setup instructions.

### Performance & Scalability (10%)

- Database optimization.
- Query ebiciency.
- Caching strategy.
- Resource usage.

## Submission Requirements

### Deliverables

1. Source Code: Complete application with all features.
2. README.md: Setup instructions, API documentation, architecture overview.
3. Tests: Comprehensive test suite with instructions to run.
4. Database: Schema migration files or setup scripts.
5. Requirements: dependencies file (`requirements.txt` or `pyproject.toml`).
6. Configuration: Environment variable documentation.

### Setup Instructions

- Setup instructions should include the following:
  - Virtual environment setup.
  - Database setup and migrations.
  - Environment variable configuration.
  - How to run the application.
  - How to run tests.
  - API endpoint documentation.

## Discussion Points (Post-Implementation)

- Be prepared to discuss the following:
  - How would you scale this system for 10,000+ concurrent users?
  - What monitoring and logging would you implement in production?
  - How would you handle HIPAA compliance and data privacy?
  - Database backup and disaster recovery strategy.
  - Performance optimization strategies.
  - Security audit considerations.

## Sample Data

- Include fixtures or sample data for the following:
  - 3-5 sample reporters.
  - 10-15 sample patients.
  - Various disease types and severity levels.
  - Reports in different states (draft, submitted, approved).
