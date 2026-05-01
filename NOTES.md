# Notes — RBAC Implementation

## Scope & Trade-offs

### What was implemented

- Full RBAC with three roles: `admin`, `manager`, `member`
- Backend enforcement via FastAPI dependency injection
- Frontend enforcement via route `beforeLoad` guards and conditional navigation
- Alembic migration replacing `is_superuser` boolean with `role` enum
- Seeded test data (admin, manager, member users)
- 9 focused backend tests covering authorization paths
- Metrics stub page (admin + manager only)
- Access denied page for unauthorized navigation
- Updated README with permission matrix and architecture docs

### What was cut

- **Playwright E2E tests**: The template has them, but they're complex to set up and outside the 1-hour scope. Backend pytest tests cover the critical auth paths.
- **Diagrams**: No Mermaid/C4 diagram (would be nice but not essential for clarity).
- **Comprehensive test coverage**: 9 well-chosen tests covering the permission matrix. In production you'd want more edge cases.
- **Backward compat with `is_superuser`**: Clean migration — old boolean replaced with enum. The migration script handles existing data.

---

## ADR-1: Dependency-Based Authorization

**Problem:** Where should authorization checks live in the FastAPI application?

**Options considered:**

1. **Middleware** — Inspect every request and check permissions in a central place
2. **Decorators** — Annotate route functions with `@requires_role("admin")`
3. **Dependencies** — Use FastAPI's `Depends()` with reusable role-check functions

**Decision:** Option 3 — FastAPI dependencies.

**Rationale:**

- Matches the existing authentication pattern (`get_current_user`, `get_current_active_superuser`)
- Role requirements are visible directly in the route decorator (`dependencies=[AdminDep]`)
- Easy to compose: `dependencies=[AdminDep]` or `dependencies=[ManagerOrAdminDep]`
- No global state or middleware complexity
- Dependencies are testable in isolation

**Trade-offs:**

- Slightly more verbose than middleware (need to annotate each route)
- But the explicitness is a feature for RBAC — it's immediately clear who can access what

---

## ADR-2: Role Storage as String Column vs Separate Permissions Table

**Problem:** How to model roles and permissions in the database?

**Options considered:**

1. **String column on User** — `role VARCHAR(20)` with enum validation
2. **Roles table + User-Role join table** — Normalized many-to-many
3. **Permissions table** — Full RBAC with granular permissions assigned to roles

**Decision:** Option 1 — String column with Python enum.

**Rationale:**

- The permission surface is small (3 roles, ~6 actions)
- No need for many-to-many complexity with only 3 roles
- Keep scope tight for a 1-hour timebox
- Easy to understand: every user has exactly one role
- Easy to extend: adding a new role is adding one enum value

**Trade-offs:**

- Not suitable for complex enterprise RBAC with dynamic role hierarchies
- If the permission matrix grows significantly, you'd want a permissions table
- For this task's scope, it's the right balance of simplicity and expressiveness

---

## What I'd Do With More Time

1. **Add a role management UI** — Allow admin users to change roles via the admin panel
2. **Add audit logging** — Log every denied access attempt (who, what, when)
3. **Add rate limiting** — Prevent brute-force attempts on auth endpoints
4. **Granular frontend permissions** — Instead of hiding nav items, show all items but disable/de-emphasize unauthorized ones
5. **End-to-end Playwright tests** — Test the full auth flow from login to protected page access
