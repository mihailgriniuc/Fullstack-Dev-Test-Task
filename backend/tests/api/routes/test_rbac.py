"""
RBAC authorization tests.

These tests verify that role-based access control is enforced correctly
for the three user roles: admin, manager, and member.

Coverage:
  - Admin: full access to user management and settings
  - Manager: can list users and view metrics, but not create/delete users
  - Member: can only access their own profile and basic features
"""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import UserRole


# ─── Helper ────────────────────────────────────────────────────────────────


def _get_token_headers_for_role(
    client: TestClient, db: Session, role: UserRole
) -> dict[str, str]:
    """Return auth headers for a user with the given role.

    Uses the seeded users from init_db():
      - admin:    settings.FIRST_SUPERUSER
      - manager:  manager@example.com
      - member:   member@example.com
    """
    email_map = {
        UserRole.ADMIN: settings.FIRST_SUPERUSER,
        UserRole.MANAGER: "manager@example.com",
        UserRole.MEMBER: "member@example.com",
    }
    email = email_map[role]
    password_map = {
        UserRole.ADMIN: settings.FIRST_SUPERUSER_PASSWORD,
        UserRole.MANAGER: "admin123",
        UserRole.MEMBER: "member123",
    }
    password = password_map[role]

    data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    tokens = r.json()
    a_token = tokens["access_token"]
    return {"Authorization": f"Bearer {a_token}"}


# ─── Tests: List users ─────────────────────────────────────────────────────


class TestListUsers:
    """GET /users/ — only admin and manager can list all users."""

    def test_admin_can_list_users(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.ADMIN)
        r = client.get(f"{settings.API_V1_STR}/users/", headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert "data" in data
        assert "count" in data

    def test_manager_can_list_users(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.MANAGER)
        r = client.get(f"{settings.API_V1_STR}/users/", headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert "data" in data
        assert "count" in data

    def test_member_cannot_list_users(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.MEMBER)
        r = client.get(f"{settings.API_V1_STR}/users/", headers=headers)
        assert r.status_code == 403
        assert r.json() == {"detail": "The user doesn't have enough privileges"}


# ─── Tests: Create user ────────────────────────────────────────────────────


class TestCreateUser:
    """POST /users/ — only admin can create users."""

    def test_admin_can_create_user(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.ADMIN)
        data = {
            "email": "newadmin@example.com",
            "password": "strongpass!1",
            "role": "member",
        }
        r = client.post(f"{settings.API_V1_STR}/users/", headers=headers, json=data)
        assert r.status_code == 200
        created = r.json()
        assert created["email"] == "newadmin@example.com"
        assert created["role"] == "member"

    def test_manager_cannot_create_user(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.MANAGER)
        data = {
            "email": "bymanager@example.com",
            "password": "strongpass!2",
        }
        r = client.post(f"{settings.API_V1_STR}/users/", headers=headers, json=data)
        assert r.status_code == 403

    def test_member_cannot_create_user(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.MEMBER)
        data = {
            "email": "bymember@example.com",
            "password": "strongpass!3",
        }
        r = client.post(f"{settings.API_V1_STR}/users/", headers=headers, json=data)
        assert r.status_code == 403


# ─── Tests: View metrics ───────────────────────────────────────────────────


class TestViewMetrics:
    """GET /metrics/ — only admin and manager can view metrics."""

    def test_admin_can_view_metrics(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.ADMIN)
        r = client.get(f"{settings.API_V1_STR}/metrics/", headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert "total_users" in data

    def test_manager_can_view_metrics(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.MANAGER)
        r = client.get(f"{settings.API_V1_STR}/metrics/", headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert "total_users" in data

    def test_member_cannot_view_metrics(self, client: TestClient, db: Session) -> None:
        headers = _get_token_headers_for_role(client, db, UserRole.MEMBER)
        r = client.get(f"{settings.API_V1_STR}/metrics/", headers=headers)
        assert r.status_code == 403
        assert r.json() == {"detail": "The user doesn't have enough privileges"}
