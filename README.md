# Full Stack FastAPI Template — RBAC Fork

This repository forks the [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) (FastAPI + React + PostgreSQL + Docker) and adds **Role-Based Access Control (RBAC)** with three roles: `admin`, `manager`, and `member`.

**AI-assisted development**: The full [pi](https://github.com/mariozechner/pi-coding-agent) AI session transcript is included as [`pi-session-2026-05-01T16-13-19-155Z_019de450-e1b3-76fa-b025-91b62a9cab6d.html`](./pi-session-2026-05-01T16-13-19-155Z_019de450-e1b3-76fa-b025-91b62a9cab6d.html) — it shows the planning, implementation, testing, and documentation process from start to finish.

---

## Quick Start

```bash
# 1. Start everything
docker compose up -d

# 2. Apply the database migration
docker compose exec backend bash -c "alembic upgrade head"

# 3. Open the app
open http://localhost:5173
```

---

## Seeded Test Users

These users are created automatically on first run:

| Email                 | Password     | Role        | Can do                   |
| --------------------- | ------------ | ----------- | ------------------------ |
| `admin@example.com`   | `changethis` | **admin**   | Everything               |
| `manager@example.com` | `admin123`   | **manager** | List users, view metrics |
| `member@example.com`  | `member123`  | **member**  | Own profile + items only |

> You can log in as any of them right after `docker compose up -d`.

---

## Permission Matrix

| Action             | admin | manager | member |
| ------------------ | ----- | ------- | ------ |
| List all users     | ✅    | ✅      | ❌     |
| Create user        | ✅    | ❌      | ❌     |
| Update any profile | ✅    | ❌      | ❌     |
| Delete users       | ✅    | ❌      | ❌     |
| View metrics       | ✅    | ✅      | ❌     |
| View own profile   | ✅    | ✅      | ✅     |
| Update own profile | ✅    | ✅      | ✅     |
| View all items     | ✅    | ❌      | ❌     |
| Create items       | ✅    | ✅      | ✅     |

---

## Frontend Behavior by Role

| Area             | admin                                    | manager                       | member               |
| ---------------- | ---------------------------------------- | ----------------------------- | -------------------- |
| **Sidebar**      | Dashboard, Items, **Metrics**, **Admin** | Dashboard, Items, **Metrics** | Dashboard, Items     |
| **Admin page**   | ✅ Full user management                  | ❌ Redirected home            | ❌ Redirected home   |
| **Metrics page** | ✅ Can view                              | ✅ Can view (view-only)       | ❌ "Access Denied"   |
| **Settings**     | My Profile, Password, **Danger zone**    | My Profile, Password          | My Profile, Password |

---

## Architecture

### Where authorization checks live

Authorization is enforced through **FastAPI dependencies** in `backend/app/api/deps.py`. The `require_role()` factory creates reusable dependency callables that check `current_user.role` against allowed roles. Convenience aliases `AdminDep` and `ManagerOrAdminDep` are provided. This matches the existing `get_current_user` pattern and makes role requirements visible directly in each route decorator:

```python
@router.get("/users/", dependencies=[ManagerOrAdminDep])
@router.post("/users/", dependencies=[AdminDep])
@router.get("/metrics/", dependencies=[ManagerOrAdminDep])
```

### How roles are stored

Roles are stored as a string column (`role`) on the `User` model using a `UserRole` Python enum (`admin`, `manager`, `member`). Default for new signups is `member`. The old `is_superuser` boolean was removed. Alembic migration `a1b2c3d4e5f6` handles the transition.

### How the frontend learns about capabilities

The `role` field is included in the `UserPublic` API response. The `useAuth` hook surfaces `user.role`, the sidebar uses it to conditionally show nav links, and route `beforeLoad` guards redirect unauthorized users. Backend is the source of truth; frontend is UX polish.

### Data flow

```
Browser  ──HTTP──>  FastAPI deps.py (get_current_user → require_role)
                         │
                         ▼
                    Routes (users.py, items.py, metrics.py)
                         │
                         ▼
                    PostgreSQL (User.role = "admin"|"manager"|"member")
```

---

## Running Tests

```bash
# All backend tests
docker compose exec backend bash scripts/tests-start.sh

# RBAC-specific tests (9 tests)
docker compose exec backend bash -c "pytest tests/api/routes/test_rbac.py -v"
```

Tests cover: admin can list/create users + view metrics, manager can list users + view metrics but NOT create users, member cannot list/create users or view metrics.

---

## Files Changed

| File                                     | What changed                                                      |
| ---------------------------------------- | ----------------------------------------------------------------- |
| **Backend**                              |                                                                   |
| `models.py`                              | Added `UserRole` enum, replaced `is_superuser` with `role` column |
| `api/deps.py`                            | Added `require_role()`, `AdminDep`, `ManagerOrAdminDep`           |
| `api/routes/users.py`                    | Role-based deps on all endpoints                                  |
| `api/routes/items.py`                    | Role-based ownership checks                                       |
| `api/routes/metrics.py`                  | **New** — metrics stub (admin + manager)                          |
| `api/routes/login.py`                    | Updated to use `AdminDep`                                         |
| `api/routes/utils.py`                    | Updated to use `AdminDep`                                         |
| `core/db.py`                             | Seeds admin + manager + member users                              |
| `alembic/versions/a1b2c3d4e5f6_*.py`     | **New** — migration: `is_superuser` → `role`                      |
| **Frontend**                             |                                                                   |
| `client/types.gen.ts` + `schemas.gen.ts` | `role` replaces `is_superuser` in generated types                 |
| `components/Admin/AddUser.tsx`           | Role dropdown replaces superuser checkbox                         |
| `components/Admin/EditUser.tsx`          | Role dropdown replaces superuser checkbox                         |
| `components/Admin/columns.tsx`           | Role badge (Admin / Manager / Member)                             |
| `components/Sidebar/AppSidebar.tsx`      | Nav items driven by `user.role`                                   |
| `components/Common/AccessDenied.tsx`     | **New** — 403 page component                                      |
| `routes/_layout/admin.tsx`               | Guard checks `role === "admin"`                                   |
| `routes/_layout/metrics.tsx`             | **New** — metrics page with guard                                 |
| `routes/_layout/access-denied.tsx`       | **New** — route for 403 page                                      |
| `routeTree.gen.ts`                       | Auto-registered new routes                                        |
| **Tests**                                |                                                                   |
| `tests/api/routes/test_rbac.py`          | **New** — 9 RBAC tests (allowed + denied for each role)           |

---

## Notes

See [`NOTES.md`](./NOTES.md) for Architecture Decision Records, scope trade-offs, and what would be done with more time.

---

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`development.md`](./development.md) for the original template's development guide.
