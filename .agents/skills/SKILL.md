---
name: fastapi-standards
description: Enforces the Goldhunga Technology (GT) FastAPI backend development standards, package design, naming conventions, layering (routers, services, repositories, models, schemas), SOLID principles, documentation requirements, and code style.
---

# FastAPI Backend Development Standards

This skill guides the agent in developing, structuring, and refactoring backend code inside the Goldhunga Technology internal system (`gt`) according to defined standards.

## Philosophy

This project prioritizes:
- Readability over cleverness
- Simplicity over abstraction
- Explicit over implicit behavior
- Maintainability over short-term convenience
- Small, focused modules over large files

Every change should leave the codebase easier to understand than before.

---

## Project Structure

Every feature must live inside its own package under `src/gt/`.
Example layout:

```text
src/gt/auth/
├── routers/
│   ├── auth_session_router.py
│   ├── auth_user_router.py
│   └── __init__.py
├── services/
│   ├── auth_service.py
│   ├── auth_user_service.py
│   └── auth_user_account_service.py
├── repositories/
│   ├── auth_base_repository.py
│   └── auth_user_repository.py
├── models/
│   ├── auth_user_model.py
│   └── auth_user_account_model.py
├── schemas/
│   └── auth_schema.py
├── dependencies/
│   └── auth_dependency.py
├── exceptions/
│   └── auth_exception.py
├── auth_uow.py
├── constants.py
├── enums.py
├── types.py
└── __init__.py
```

Packages should be self-contained and own their business logic. Do not place unrelated functionality inside another package.

---

## File Naming Convention

Every file **must begin with the package name** (e.g., `auth_`).

Examples:
- `auth_router.py` / `auth_user_router.py`
- `auth_service.py` / `auth_user_service.py`
- `auth_repository.py` / `auth_user_repository.py`
- `auth_model.py` / `auth_user_model.py`
- `auth_schema.py` / `auth_user_schema.py`
- `auth_dependency.py` / `auth_user_dependency.py`
- `auth_exception.py`

Avoid generic filenames like `router.py`, `service.py`, `repository.py`, `model.py`, `schema.py`, `utils.py`, `helpers.py`, `common.py`, `misc.py`. A filename should clearly describe its purpose.

---

## File Size

A source file **must not exceed 200 lines**. If a file approaches this limit, split it by responsibility (e.g., separate services or split router paths). Never create "God files."

---

## SOLID Principles

All code must follow SOLID principles:
- **Single Responsibility**: Each class/function should have one responsibility/task.
- **Open/Closed**: Prefer extending behavior rather than modifying existing implementations.
- **Liskov Substitution**: Derived implementations must behave consistently with their abstractions.
- **Interface Segregation**: Keep interfaces focused and minimal.
- **Dependency Inversion**: Depend on abstractions rather than concrete implementations whenever appropriate.

---

## Layer Responsibilities

### Router
The router is intentionally **thin**. It should only:
- Receive the request
- Resolve dependencies
- Create or receive the Unit of Work (if applicable)
- Call the appropriate service
- Return the response

A router must **never**:
- Contain business logic or validate business rules
- Query the database or build SQL
- Manipulate ORM models
- Perform calculations or call external APIs directly

### Service
Services own all business logic.
- Business rules, validation, and authorization decisions.
- Calling repositories and coordinating transactions.
- Services should never know about HTTP. No FastAPI request/response or status objects should exist inside services.

### Repository
Repositories only interact with database/persistence.
- Query, create, update, or delete records.
- Repositories should never contain business logic.
- Repositories should never commit transactions.

### Unit of Work
The Unit of Work owns:
- Database session and transaction boundaries.
- Repositories must never call `commit()`. Only the Unit of Work controls transactions.

### Schema
Schemas define request and response models only. No business logic. No database access.

### Model
Models define persistence only. No validation logic. No API serialization. No business logic.

### Dependency
Contains FastAPI dependency providers only (e.g., `get_current_user`, permissions, db session).

### Exceptions
Every package owns its own exceptions. Avoid generic exceptions.

---

## Function Design
Functions should:
- Do one thing
- Be easy to read
- Have descriptive names (e.g., `verify_password()`, not `process()`)
- Avoid side effects whenever possible

---

## Class Design
Classes should be:
- Small
- Focused
- Easily testable

Avoid classes responsible for multiple domains.

---

## Documentation
- Every class **must** have a docstring.
- Every function **must** have a docstring.
- Every public method **must** have a docstring.
- Every complex algorithm should include comments explaining **why**, not **what**.

---

## Dependency Injection
Never instantiate dependencies inside services. Inject them instead (e.g., pass repository to service `__init__`).

---

## Type Hints
- Every function must include complete type hints.
- Every return type must be declared.
- Avoid `Any` unless absolutely necessary.

---

## Constants
Never hardcode values. Use capitalized constants (e.g. `MAX_LOGIN_ATTEMPTS = 5`).

---

## Logging
Log meaningful events (e.g., login, logout, password reset, failures).
Never log passwords, tokens, secrets, API keys, or sensitive personal information.

---

## Error Handling
Raise meaningful domain exceptions. Do not silently ignore failures or return `None` for exceptional situations.

---

## Database & Async Rules
- Repositories should avoid N+1 queries.
- Keep async all the way down.
- Never perform blocking I/O inside async code. Await every database operation.

---

## Configuration
Configuration should come from a centralized settings module. Never call environment variables directly throughout the project.

---

## Code Style
Prefer:
- Early returns
- Small functions
- Small classes
- Explicit code
- Descriptive variable names

Avoid:
- Deep nesting
- Boolean flag parameters
- Large constructors
- Hidden side effects

---

## Package Boundaries
Packages should remain independent. Do not directly access another package's repositories or internal implementation. Interact through public services or interfaces.

---

## Pull Request Checklist
Before merging, ensure:
- [ ] File is under 200 lines.
- [ ] SOLID principles are followed.
- [ ] Every class, function, and public method has a docstring.
- [ ] Router contains only request handling, service invocation, and response. No business logic/SQL in routers.
- [ ] Repositories never commit transactions.
- [ ] Complete type hints are present.
- [ ] No duplicated logic.
- [ ] No wildcard/unused imports.
- [ ] Async code contains no blocking operations.
- [ ] The code is simpler than before it was modified.
