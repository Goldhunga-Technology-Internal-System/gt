# GT Auth

> **A batteries-included authentication framework for FastAPI.**

GT Auth is a modern authentication framework designed to eliminate the repetitive work involved in building authentication systems.

It integrates directly with your existing **FastAPI**, **SQLAlchemy**, and **Alembic** project without forcing a new project structure.

> **Status:** Public Preview (v1). APIs may evolve based on community feedback.

---

# Features

## Current

- FastAPI integration
- SQLAlchemy integration
- Dynamic authentication models
- Alembic-compatible migrations
- Policy-based route protection
- Current user dependency
- Session management foundation

## Planned

- MFA
- Email verification
- Password reset
- OAuth/Social login
- RBAC
- Organizations
- API Keys
- Audit Logs
- Background jobs
- Email utilities

---

# Installation

Currently GT Auth is distributed directly from GitHub.

```bash
uv add git+https://github.com/<ORG>/<REPO>.git
```

---

# Quick Start

```python
from fastapi import Depends, FastAPI
from gt.auth import Auth

from app.core.database import Base, async_session_factory

app = FastAPI(title="Trash", version="0.1.0")

auth = Auth(
    base=Base,
    session_factory=async_session_factory,
)

auth.register_policy(
    name="minimum",
    checks=[],
)

auth.init_app(app)


@app.get("/me")
@auth.policy("minimum")
async def me(user=Depends(auth.current_user())):
    return {"email": user.email}
```

---

# Creating Authentication Models

Import the model factories.

```python
from app.models import Base

from gt.auth.models import (
    create_auth_user_model,
    create_auth_user_account_model,
    create_auth_user_onboarding_model,
    create_auth_user_session_model,
    create_auth_user_tokens_model,
)
```

Register the authentication models.

```python
User = create_auth_user_model(Base)

create_auth_user_account_model(Base, User)
create_auth_user_onboarding_model(Base, User)
create_auth_user_session_model(Base, User)
create_auth_user_tokens_model(Base, User)
```

These models become part of your application's metadata, allowing Alembic to discover them automatically.

---

# Alembic Integration

Ensure your models are imported before `target_metadata` is evaluated.

```python
from app.models import Base

target_metadata = Base.metadata
```

Generate a migration:

```bash
alembic revision --autogenerate -m "Create auth tables"
```

Apply it:

```bash
alembic upgrade head
```

---

# Design Philosophy

GT Auth **does not create a separate authentication database**.

Instead it attaches authentication models to your existing SQLAlchemy `Base`.

Benefits:

- One metadata
- One migration history
- One Alembic project
- One database
- No duplicated models

---

# Roadmap

- [x] FastAPI support
- [x] SQLAlchemy support
- [x] Policies
- [x] Sessions
- [x] Email verification
- [ ] MFA
- [ ] OAuth
- [ ] Background jobs
- [ ] Email service
- [ ] RBAC
- [ ] Organizations

---

# Contributing

Issues, feature requests and pull requests are welcome.

---

# License

MIT
