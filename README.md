# Full Stack FastAPI Template

<a href="https://github.com/fastapi/full-stack-fastapi-template/actions?query=workflow%3A%22Test+Docker+Compose%22" target="_blank"><img src="https://github.com/fastapi/full-stack-fastapi-template/workflows/Test%20Docker%20Compose/badge.svg" alt="Test Docker Compose"></a>
<a href="https://github.com/fastapi/full-stack-fastapi-template/actions?query=workflow%3A%22Test+Backend%22" target="_blank"><img src="https://github.com/fastapi/full-stack-fastapi-template/workflows/Test%20Backend/badge.svg" alt="Test Backend"></a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/full-stack-fastapi-template" target="_blank"><img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/full-stack-fastapi-template.svg" alt="Coverage"></a>

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
  - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [React](https://react.dev) for the frontend.
  - 💃 Using TypeScript, hooks, [Vite](https://vitejs.dev), and other parts of a modern frontend stack.
  - 🎨 [Tailwind CSS](https://tailwindcss.com) and [shadcn/ui](https://ui.shadcn.com) for the frontend components.
  - 🤖 An automatically generated frontend client.
  - 🧪 [Playwright](https://playwright.dev) for End-to-End testing.
  - 🦇 Dark mode support.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email based password recovery.
- 📬 [Mailcatcher](https://mailcatcher.me) for local email testing during development.
- ✅ Tests with [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

### Dashboard Login

[![API docs](img/login.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Admin

[![API docs](img/dashboard.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Items

[![API docs](img/dashboard-items.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Dark Mode

[![API docs](img/dashboard-dark.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Interactive API Documentation

[![API docs](img/docs.png)](https://github.com/fastapi/full-stack-fastapi-template)

## How To Use It

You can **just fork or clone** this repository and use it as is.

✨ It just works. ✨

### How to Use a Private Repository

If you want to have a private repository, GitHub won't allow you to simply fork it as it doesn't allow changing the visibility of forks.

But you can do the following:

- Create a new GitHub repo, for example `my-full-stack`.
- Clone this repository manually, set the name with the name of the project you want to use, for example `my-full-stack`:

```bash
git clone git@github.com:fastapi/full-stack-fastapi-template.git my-full-stack
```

- Enter into the new directory:

```bash
cd my-full-stack
```

- Set the new origin to your new repository, copy it from the GitHub interface, for example:

```bash
git remote set-url origin git@github.com:octocat/my-full-stack.git
```

- Add this repo as another "remote" to allow you to get updates later:

```bash
git remote add upstream git@github.com:fastapi/full-stack-fastapi-template.git
```

- Push the code to your new repository:

```bash
git push -u origin master
```

### Update From the Original Template

After cloning the repository, and after doing changes, you might want to get the latest changes from this original template.

- Make sure you added the original repository as a remote, you can check it with:

```bash
git remote -v

origin    git@github.com:octocat/my-full-stack.git (fetch)
origin    git@github.com:octocat/my-full-stack.git (push)
upstream    git@github.com:fastapi/full-stack-fastapi-template.git (fetch)
upstream    git@github.com:fastapi/full-stack-fastapi-template.git (push)
```

- Pull the latest changes without merging:

```bash
git pull --no-commit upstream master
```

This will download the latest changes from this template without committing them, that way you can check everything is right before committing.

- If there are conflicts, solve them in your editor.

- Once you are done, commit the changes:

```bash
git merge --continue
```

### Configure

You can then update configs in the `.env` files to customize your configurations.

Before deploying it, make sure you change at least the values for:

- `SECRET_KEY`
- `FIRST_SUPERUSER_PASSWORD`
- `POSTGRES_PASSWORD`

You can (and should) pass these as environment variables from secrets.

Read the [deployment.md](./deployment.md) docs for more details.

### Generate Secret Keys

Some environment variables in the `.env` file have a default value of `changethis`.

You have to change them with a secret key, to generate secret keys you can run the following command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the content and use that as password / secret key. And run that again to generate another secure key.

## How To Use It - Alternative With Copier

This repository also supports generating a new project using [Copier](https://copier.readthedocs.io).

It will copy all the files, ask you configuration questions, and update the `.env` files with your answers.

### Install Copier

You can install Copier with:

```bash
pip install copier
```

Or better, if you have [`pipx`](https://pipx.pypa.io/), you can run it with:

```bash
pipx install copier
```

**Note**: If you have `pipx`, installing copier is optional, you could run it directly.

### Generate a Project With Copier

Decide a name for your new project's directory, you will use it below. For example, `my-awesome-project`.

Go to the directory that will be the parent of your project, and run the command with your project's name:

```bash
copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```

If you have `pipx` and you didn't install `copier`, you can run it directly:

```bash
pipx run copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```

**Note** the `--trust` option is necessary to be able to execute a [post-creation script](https://github.com/fastapi/full-stack-fastapi-template/blob/master/.copier/update_dotenv.py) that updates your `.env` files.

### Input Variables

Copier will ask you for some data, you might want to have at hand before generating the project.

But don't worry, you can just update any of that in the `.env` files afterwards.

The input variables, with their default values (some auto generated) are:

- `project_name`: (default: `"FastAPI Project"`) The name of the project, shown to API users (in .env).
- `stack_name`: (default: `"fastapi-project"`) The name of the stack used for Docker Compose labels and project name (no spaces, no periods) (in .env).
- `secret_key`: (default: `"changethis"`) The secret key for the project, used for security, stored in .env, you can generate one with the method above.
- `first_superuser`: (default: `"admin@example.com"`) The email of the first superuser (in .env).
- `first_superuser_password`: (default: `"changethis"`) The password of the first superuser (in .env).
- `smtp_host`: (default: "") The SMTP server host to send emails, you can set it later in .env.
- `smtp_user`: (default: "") The SMTP server user to send emails, you can set it later in .env.
- `smtp_password`: (default: "") The SMTP server password to send emails, you can set it later in .env.
- `emails_from_email`: (default: `"info@example.com"`) The email account to send emails from, you can set it later in .env.
- `postgres_password`: (default: `"changethis"`) The password for the PostgreSQL database, stored in .env, you can generate one with the method above.
- `sentry_dsn`: (default: "") The DSN for Sentry, if you are using it, you can set it later in .env.

## Backend Development

Backend docs: [backend/README.md](./backend/README.md).

## Frontend Development

Frontend docs: [frontend/README.md](./frontend/README.md).

## Deployment

Deployment docs: [deployment.md](./deployment.md).

## Development

General development docs: [development.md](./development.md).

This includes using Docker Compose, custom local domains, `.env` configurations, etc.

## Role-Based Access Control (RBAC)

This fork adds role-based access control (RBAC) on top of the [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template).

### Quick Start

```bash
# 1. Start the stack
docker compose up -d

# 2. Apply the RBAC migration
docker compose exec backend bash -c "alembic upgrade head"

# 3. Open the app at http://localhost:5173
```

### Roles

| Role        | Description                                                                |
| ----------- | -------------------------------------------------------------------------- |
| **admin**   | Full access to user management, settings, metrics, and all items           |
| **manager** | Can list users and view metrics, but cannot create/update/delete users     |
| **member**  | Can only access their own profile, their own items, and basic app features |

### Permission Matrix

| Action             | admin | manager | member |
| ------------------ | ----- | ------- | ------ |
| List all users     | ✅    | ✅      | ❌     |
| Create user        | ✅    | ❌      | ❌     |
| Update any profile | ✅    | ❌      | ❌     |
| Delete users       | ✅    | ❌      | ❌     |
| View metrics       | ✅    | ✅      | ❌     |
| View own profile   | ✅    | ✅      | ✅     |
| Update own profile | ✅    | ✅      | ✅     |
| Create items       | ✅    | ✅      | ✅     |
| View all items     | ✅    | ❌      | ❌     |

### Seeded Test Users

These users are created automatically on first database initialization:

| Email                 | Password     | Role        | Notes                                  |
| --------------------- | ------------ | ----------- | -------------------------------------- |
| `admin@example.com`   | `changethis` | **admin**   | Full access. Change password in `.env` |
| `manager@example.com` | `admin123`   | **manager** | Can list users, view metrics           |
| `member@example.com`  | `member123`  | **member**  | Own profile + items only               |

> To add more seed users, edit `backend/app/core/db.py` → `init_db()`.

### Frontend Behavior by Role

| Area             | admin                                        | manager                                   | member                         |
| ---------------- | -------------------------------------------- | ----------------------------------------- | ------------------------------ |
| **Sidebar**      | Dashboard, Items, **Metrics**, **Admin**     | Dashboard, Items, **Metrics**             | Dashboard, Items               |
| **Admin page**   | ✅ Full user management (list, create, edit) | ❌ Redirected to home                     | ❌ Redirected to home          |
| **Metrics page** | ✅ Can view metrics                          | ✅ Can view metrics (view-only indicator) | ❌ Redirected to access denied |
| **Settings**     | My Profile, Password, **Danger zone**        | My Profile, Password                      | My Profile, Password           |

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React)                   │
│  ┌──────────┐   ┌──────────────┐   ┌────────────┐  │
│  │ Sidebar  │   │ beforeLoad   │   │ useAuth    │  │
│  │ (nav     │   │ (route guard)│   │ (user.role)│  │
│  │  items)  │   │              │   │            │  │
│  └──────────┘   └──────────────┘   └────────────┘  │
│         │               │                  ▲        │
│         ▼               ▼                  │        │
│  ┌─────────────────────────────────────────┴───┐    │
│  │           HTTP API (generated client)       │    │
│  └───────────────────┬─────────────────────────┘    │
└──────────────────────┼──────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────┐
│                      ▼                              │
│  ┌──────────────────────────────────────────────┐   │
│  │         FastAPI Backend                       │   │
│  │                                               │   │
│  │  ┌──────────────────────────────────────┐     │   │
│  │  │  Dependencies (deps.py)              │     │   │
│  │  │  ┌──────────┐  ┌────────────────┐    │     │   │
│  │  │  │get_current│  │require_role()  │    │     │   │
│  │  │  │_user     │  │AdminDep        │    │     │   │
│  │  │  │          │  │ManagerOrAdminDep│   │     │   │
│  │  │  └──────────┘  └────────────────┘    │     │   │
│  │  └──────────────────────────────────────┘     │   │
│  │         │                                     │   │
│  │         ▼                                     │   │
│  │  ┌──────────────────────────────────────┐     │   │
│  │  │  Routes (users.py, items.py,         │     │   │
│  │  │           metrics.py)                │     │   │
│  │  │  dependencies=[AdminDep]             │     │   │
│  │  │  dependencies=[ManagerOrAdminDep]    │     │   │
│  │  └──────────────────────────────────────┘     │   │
│  │         │                                     │   │
│  │         ▼                                     │   │
│  │  ┌──────────────────────────────────────┐     │   │
│  │  │  SQLModel / PostgreSQL               │     │   │
│  │  │  User.role = "admin"|"manager"|"member"│    │   │
│  │  └──────────────────────────────────────┘     │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Where authorization checks live:**
Authorization is enforced through **FastAPI dependencies** in `backend/app/api/deps.py`.
The `require_role()` factory function creates reusable dependency callables that check
`current_user.role` against a list of allowed roles. Convenience aliases `AdminDep` and
`ManagerOrAdminDep` are provided for common combinations. This approach is consistent
with the existing `get_current_user` pattern and makes role requirements visible directly
in each route decorator.

**How roles are stored and validated:**
Roles are stored as a string column (`role`) on the `User` model, using a `UserRole`
Python enum (`admin`, `manager`, `member`). The default role for new signups is `member`.
The old `is_superuser` boolean has been replaced by this enum. An Alembic migration
(`a1b2c3d4e5f6`) handles the schema change and migrates existing data.

**How the frontend learns about user capabilities:**
The `role` field is included in the `UserPublic` response model, so the frontend receives
it via `GET /users/me` on every page load. The `useAuth` hook surfaces `user.role`,
which the sidebar uses to conditionally show navigation links, and route `beforeLoad`
guards use to redirect unauthorized users.

### Running Tests

```bash
# Run all backend tests
docker compose exec backend bash scripts/tests-start.sh

# Run only the RBAC authorization tests
docker compose exec backend bash -c "pytest tests/api/routes/test_rbac.py -v"

# Expected output:
# test_admin_can_list_users ......... PASSED
# test_manager_can_list_users ....... PASSED
# test_member_cannot_list_users ..... PASSED
# test_admin_can_create_user ........ PASSED
# test_manager_cannot_create_user ... PASSED
# test_member_cannot_create_user .... PASSED
# test_admin_can_view_metrics ....... PASSED
# test_manager_can_view_metrics ..... PASSED
# test_member_cannot_view_metrics ... PASSED
```

### Files Changed / Added

| File                                              | Change                                                     |
| ------------------------------------------------- | ---------------------------------------------------------- |
| `backend/app/models.py`                           | Added `UserRole` enum, replaced `is_superuser` with `role` |
| `backend/app/api/deps.py`                         | Added `require_role()`, `AdminDep`, `ManagerOrAdminDep`    |
| `backend/app/api/routes/users.py`                 | Updated all endpoints with role-based deps                 |
| `backend/app/api/routes/items.py`                 | Updated ownership checks to use role                       |
| `backend/app/api/routes/metrics.py`               | **New** — metrics stub for admin + manager                 |
| `backend/app/api/main.py`                         | Registered metrics router                                  |
| `backend/app/core/db.py`                          | Seed 3 users (admin, manager, member)                      |
| `backend/app/alembic/versions/a1b2c3d4e5f6_*.py`  | **New** — migration: `is_superuser` → `role`               |
| `frontend/src/client/types.gen.ts`                | Updated types: `role` replaces `is_superuser`              |
| `frontend/src/client/schemas.gen.ts`              | Updated schemas: `role` replaces `is_superuser`            |
| `frontend/src/components/Admin/AddUser.tsx`       | Role dropdown replaces superuser checkbox                  |
| `frontend/src/components/Admin/EditUser.tsx`      | Role dropdown replaces superuser checkbox                  |
| `frontend/src/components/Admin/columns.tsx`       | Role badge (Admin/Manager/Member)                          |
| `frontend/src/components/Sidebar/AppSidebar.tsx`  | Role-based nav items                                       |
| `frontend/src/components/Common/AccessDenied.tsx` | **New** — 403 page component                               |
| `frontend/src/routes/_layout/admin.tsx`           | Route guard checks `role === "admin"`                      |
| `frontend/src/routes/_layout/metrics.tsx`         | **New** — metrics page with route guard                    |
| `frontend/src/routes/_layout/access-denied.tsx`   | **New** — access denied route                              |
| `frontend/src/routes/_layout/settings.tsx`        | Danger zone tab only for admin                             |
| `backend/tests/api/routes/test_rbac.py`           | **New** — 9 RBAC authorization tests                       |
| `NOTES.md`                                        | **New** — ADRs, trade-offs, future work                    |

### Notes

See [`NOTES.md`](./NOTES.md) for:

- Architecture Decision Records (ADRs)
- Scope cuts and trade-offs
- What would be done with more time

## Release Notes

Check the file [release-notes.md](./release-notes.md).

## License

The Full Stack FastAPI Template is licensed under the terms of the MIT license.
