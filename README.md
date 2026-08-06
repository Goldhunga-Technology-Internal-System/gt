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
uv add git+https://github.com/Goldhunga-Technology-Internal-System/gt.git
```

---

# Quick Start

## 1. Create the Auth instance

```python
from fastapi import Depends, FastAPI
from gt.auth import Auth

from app.core.database import Base, async_session_factory

app = FastAPI(title="My App", version="0.1.0")

auth = Auth(
    base=Base,
    session_factory=async_session_factory,
)
```

The `Auth` constructor accepts the following parameters:

| Parameter                    | Required | Default                                    | Description                                                        |
| ---------------------------- | -------- | ------------------------------------------ | ------------------------------------------------------------------ |
| `base`                       | Yes      | —                                          | Your application's SQLAlchemy `DeclarativeBase` (metadata owner).   |
| `session_factory`            | Yes      | —                                          | An `async_sessionmaker[AsyncSession]` from your database setup.     |
| `settings`                   | No       | `AuthSettings()`                           | Configuration for cookies, sessions and email verification tokens.  |
| `user_model`                 | No       | `AuthUserModel`                            | Custom user model to override the default. **Reserved for v2.**     |
| `user_onboarding_model`      | No       | `AuthUserOnboardingModelBase`              | Custom onboarding model. **Reserved for v2.**                       |
| `user_register_schema`       | No       | `AuthUserRegisterSchema`                   | Custom registration schema. **Reserved for v2.**                    |
| `onboarding_register_schema` | No       | `AuthOnboardingRegisterSchema`             | Custom onboarding registration schema. **Reserved for v2.**         |

> **Important:** In v1 you should **not** pass a custom `user_model`, `user_onboarding_model`, `user_register_schema`, or `onboarding_register_schema` — use the defaults. Support for overriding these will be available in **v2**.

## 2. Register a policy

A policy is a named set of checks that protects your routes.

```python
auth.register_policy(
    name="minimum",
    checks=[],
)
```

Available checks: `mfa_required`, `email_verified`, `onboarded`.

## 3. Initialize the app

```python
auth.init_app(app)
```

`auth.init_app(app)` registers the authentication routers (register, login, logout, email verification, etc.) and the custom exception handlers onto your FastAPI application.

### Use Auth as a singleton

Because `Auth` wires up your models, settings, routers and dependencies, it is best to create **one** instance and reuse it across your project — e.g. in a shared module — rather than constructing a new one in every file.

```python
# app/security/auth.py
from gt.auth import Auth

from app.core.database import Base, async_session_factory

auth = Auth(
    base=Base,
    session_factory=async_session_factory,
)
```

Then import the same instance anywhere:

```python
from app.security.auth import auth

auth.register_policy(name="minimum", checks=[])


@app.get("/me")
@auth.policy("minimum")
async def me(user=Depends(auth.current_user())):
    return {"email": user.email}
```

## 4. Protect a route

```python
@app.get("/me")
@auth.policy("minimum")
async def me(user=Depends(auth.current_user())):
    return {"email": user.email}
```

---

# Configuration

## AuthSettings

Authentication behaviour is controlled through `AuthSettings`, passed to `Auth` via the `settings` argument. All fields have sensible defaults:

| Field                                   | Default         | Description                                                    |
| --------------------------------------- | --------------- | -------------------------------------------------------------- |
| `cookie_domain`                         | `None`          | Domain for the session cookie.                                 |
| `cookie_path`                           | `"/"`           | Path for the session cookie.                                   |
| `cookie_secure`                         | `True`          | Only send the cookie over HTTPS. Set `False` for local dev.    |
| `cookie_httponly`                       | `True`          | Prevent JavaScript from reading the cookie.                    |
| `cookie_samesite`                       | `"lax"`         | SameSite policy: `lax`, `strict` or `none`.                    |
| `session_expiration_minutes`            | `10080` (7 days) | How long a session stays valid.                               |
| `email_verification_token_expiry_minutes` | `15`            | Expiry of email verification tokens.                           |
| `email_verification_token_digit`        | `6`             | Number of digits in the email verification token.              |

Example:

```python
from gt.auth import Auth
from gt.auth.settings import AuthSettings

auth = Auth(
    base=Base,
    session_factory=async_session_factory,
    settings=AuthSettings(
        cookie_secure=False,  # for local HTTP development
        session_expiration_minutes=60 * 24 * 30,  # 30 days
    ),
)
```

---

# Session Flow

GT Auth uses cookie-based sessions. Here is how the flow works:

1. **Register or login** — `POST /auth/register` or `POST /auth/login` creates a new session and returns it to the client as an `session_uuid` cookie (HTTP-only).
2. **Browser stores the cookie** — all subsequent requests automatically include it.
3. **Protected routes** — `Depends(auth.current_user())` reads the `session_uuid` cookie, looks up the session in the database, and resolves the authenticated user.
4. **Logout** — `POST /auth/logout` deactivates the session and clears the cookie.

Session behaviour is controlled through `AuthSettings`:

- `session_expiration_minutes` — how long a session stays valid.
- `cookie_secure` / `cookie_httponly` / `cookie_samesite` / `cookie_domain` / `cookie_path` — cookie flags.

> **Note:** In development over plain `http://localhost`, set `cookie_secure=False`, otherwise the browser will refuse to store the session cookie.

---

# API Endpoints

`auth.init_app(app)` mounts all authentication routes under the `/auth` prefix.

## Authentication Core

| Method | Endpoint                     | Auth required | Body                                         | Description                                |
| ------ | ---------------------------- | ------------- | -------------------------------------------- | ------------------------------------------ |
| POST   | `/auth/register`             | No            | `email`, `password`, `full_name?`, `avatar_bg?` | Creates a user and starts a session (sets `session_uuid` cookie). |
| POST   | `/auth/login`                | No            | `email`, `password`                          | Logs the user in and sets `session_uuid` cookie. |
| POST   | `/auth/logout`               | No            | —                                            | Deactivates the session and clears the cookie. |

## Authentication Email

| Method | Endpoint                          | Auth required | Body        | Description                                   |
| ------ | --------------------------------- | ------------- | ----------- | --------------------------------------------- |
| POST   | `/auth/email-verification`        | Yes           | `token`     | Verifies the user's email address.            |
| POST   | `/auth/resend-email-verification` | Yes           | —           | Generates a new token and re-triggers the email event. |

## Authentication Onboarding

| Method | Endpoint          | Auth required                | Body                                  | Description                        |
| ------ | ----------------- | ---------------------------- | ------------------------------------- | ---------------------------------- |
| POST   | `/auth/onboarding` | Yes (email verified, not onboarded) | `theme?`, `referral_source?` | Marks the user as onboarded.       |

---

# Events

GT Auth is event-driven. When actions happen it **publishes domain events** on an in-memory event bus — but it does **not** send emails itself.

> **Why am I not receiving emails?** GT Auth does not deliver emails. It only publishes events such as `UserCreatedEvent`. You must subscribe to those events and send the emails yourself. This keeps GT Auth decoupled from your email provider.

## Available events

| Event                                  | Published when                                          | Payload highlights                                      |
| -------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| `UserCreatedEvent`                     | A user registers via `/auth/register`                   | `user_id`, `email`, `full_name`, `user_uuid`, `email_token`, `email_token_expiry_minutes` |
| `UserEmailVerifiedEvent`               | A user's email is successfully verified                  | `user_id`, `email`, `user_uuid`                          |
| `UserEmailVerificationResentEvent`     | A verification token is resent                           | `user_id`, `email`, `full_name`, `user_uuid`, `email_token`, `email_token_expiry_minutes` |

> The `email_token` in `UserCreatedEvent` and `UserEmailVerificationResentEvent` is what you send to the user; the expiry is in `email_token_expiry_minutes`.

## Subscribing with the `@auth.on` decorator

Register handlers on the shared `auth` singleton — they run whenever the matching event is published.

```python
from gt.auth.events import UserCreatedEvent


@auth.on(UserCreatedEvent)
async def send_verification_email(event: UserCreatedEvent):
    await email_service.send(
        to=event.email,
        subject="Verify your email",
        body=f"Your verification code is {event.email_token}",
    )
```

## Subscribing directly on the event bus

Handlers are async or sync functions registered per event type:

```python
from gt.auth.events import event_bus, UserEmailVerifiedEvent


async def on_email_verified(event: UserEmailVerifiedEvent):
    await analytics.track("email_verified", user_id=event.user_id)


event_bus.register(UserEmailVerifiedEvent, on_email_verified)
```

---

# Creating Authentication Models

The authentication tables are created through model factories. Register these **in your `alembic/env.py` file** so that Alembic discovers them before `target_metadata` is evaluated:

```python
# alembic/env.py
from app.models import Base

from gt.auth.models import (
    create_auth_user_model,
    create_auth_user_account_model,
    create_auth_user_onboarding_model,
    create_auth_user_session_model,
    create_auth_user_tokens_model,
)

User = create_auth_user_model(Base)

create_auth_user_account_model(Base, User)
create_auth_user_onboarding_model(Base, User)
create_auth_user_session_model(Base, User)
create_auth_user_tokens_model(Base, User)

target_metadata = Base.metadata
```

These models become part of your application's metadata, allowing Alembic to discover them automatically.

---

# Alembic Integration

Ensure your models are imported before `target_metadata` is evaluated (see above).

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
