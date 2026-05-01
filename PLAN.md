# RBAC Implementation Plan

## Overview

Add Role-Based Access Control (RBAC) to the [Full-Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template) so that only authorized users can access sensitive endpoints and UI sections.

**Timebox**: ~1 hour

---

## Current State

The template already has:

- JWT-based authentication (`get_current_user` dependency)
- A `is_superuser` boolean on the `User` model (binary superuser/non-superuser split)
- Frontend auth via `useAuth` hook, `isLoggedIn()` check, and `beforeLoad` route guards
- Admin route + sidebar link conditionally shown based on `is_superuser`

**What's missing**: A proper role system (admin / manager / member) with granular permissions.

---

## Permission Matrix

| Action             | admin | manager | member |
| ------------------ | ----- | ------- | ------ |
| List all users     | ✅    | ✅      | ❌     |
| Create user        | ✅    | ❌      | ❌     |
| View metrics       | ✅    | ✅      | ❌     |
| Update own profile | ✅    | ✅      | ✅     |
| Update any profile | ✅    | ❌      | ❌     |

---

## Implementation Plan

### Phase 1 — Backend Model Changes (~10 min)

1. **Add `UserRole` enum** in `backend/app/models.py`:
   - `admin`, `manager`, `member`

2. **Add `role` column** to the `User` table:
   - Default: `member`
   - Include in `UserPublic` response model so frontend knows the role
   - Keep `is_superuser` for backward compat or deprecate it

3. **Generate Alembic migration**:
   ```bash
   alembic revision --autogenerate -m "Add role column to User"
   alembic upgrade head
   ```

### Phase 2 — Backend Auth Dependencies (~8 min)

4. **Add role-check dependencies** in `backend/app/api/deps.py`:
   - `get_current_admin()` — requires role == admin
   - `get_current_manager_or_admin()` — requires role in [admin, manager]
   - Generic `RoleChecker(required_roles: list[str])` factory for flexibility

### Phase 3 — Backend API Routes (~10 min)

5. **Update `users.py` router**:
   - `GET /users/` — change from `get_current_active_superuser` → `get_current_manager_or_admin`
   - `POST /users/` — change from `get_current_active_superuser` → `get_current_admin`
   - `GET /me` / `PATCH /me` — keep as `CurrentUser` (any authenticated user)
   - `PATCH /{user_id}` / `DELETE /{user_id}` — change to `get_current_admin`

6. **Add `metrics.py` router** with a stub endpoint:
   - `GET /metrics/` — protected for admin + manager
   - Returns simple placeholder data (e.g. `{"total_users": 0, "active_users": 0}`)

7. **Register the new router** in `backend/app/api/main.py`

### Phase 4 — Seed Data (~5 min)

8. **Update `backend/app/core/db.py` (init_db)**:
   - Seed at least one admin user (e.g. `admin@example.com`)
   - Seed at least one non-admin user (e.g. `manager@example.com` with role=manager)
   - Seed a regular member user (e.g. `member@example.com`)

### Phase 5 — Frontend Changes (~12 min)

9. **Update `AppSidebar.tsx`**:
   - Use `user.role` instead of `user.is_superuser` for showing Admin link
   - Add a "Metrics" nav item visible to admin + manager

10. **Add `/metrics` route** (`frontend/src/routes/_layout/metrics.tsx`):
    - Simple stub page showing placeholder metrics
    - `beforeLoad` guard: redirect if role not in [admin, manager]
    - Show "Access Denied" page for unauthorized direct navigation

11. **Update `admin.tsx` `beforeLoad` guard**:
    - Change from `is_superuser` check to `role === "admin"` check

12. **Update settings page** if needed:
    - Ensure "Danger zone" tab only shows for admin (align with role)

### Phase 6 — Testing (~10 min)

13. **Write 3 focused backend tests** in `backend/tests/`:
    - **Test 1**: Admin can list users → 200
    - **Test 2**: Member cannot list users → 403
    - **Test 3**: Admin can create a user → 200, Manager cannot → 403

### Phase 7 — Documentation (~5 min)

14. **Update `README.md`**:
    - Permission matrix (table above)
    - Brief architecture explanation (2-4 paragraphs):
      - Where authorization checks live (dependencies)
      - How roles are stored and validated (DB column + enum)
      - How frontend learns about user capabilities (role in UserPublic)
    - How to run locally, seed data, run tests

15. **Optional: Create `NOTES.md`** with:
    - ADR for dependency-based auth vs middleware/decorator approach
    - Scope cuts (if any)
    - What would be done with more time

---

## Architecture Decisions

| Decision             | Choice                                    | Rationale                                                                                                       |
| -------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Where checks live    | FastAPI dependencies                      | Matches existing pattern (`get_current_user`, `get_current_active_superuser`). Easy to compose, test, and read. |
| Role storage         | DB enum column on `User`                  | Simple, no extra tables. Fits the scope. For more complex RBAC you'd want a roles/permissions table.            |
| Frontend enforcement | `beforeLoad` guards + conditional sidebar | Matches existing pattern. Backend is the source of truth; frontend is UX polish.                                |
| Tests                | Pytest with `TestClient`                  | Already set up in the template. Focus on 3 critical auth paths.                                                 |

---

## What We'd Cut If Short on Time

- ❌ Playwright E2E tests → stick to backend pytest tests
- ❌ Fancy diagrams → skip or quick Mermaid
- ❌ Comprehensive test coverage → 3 well-chosen tests is enough
- ❌ Backward compatibility with `is_superuser` → clean migration

**Never cut**: Security enforcement on the backend, README setup instructions, consistent frontend/backend role mapping.
