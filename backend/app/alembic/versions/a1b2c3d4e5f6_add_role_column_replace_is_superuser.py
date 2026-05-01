"""Add role column, replace is_superuser with role-based RBAC.

Revision ID: a1b2c3d4e5f6
Revises: fe56fa70289e
Create Date: 2026-05-01 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "fe56fa70289e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the new `role` column with a default of 'member'
    op.add_column(
        "user",
        sa.Column(
            "role",
            sqlmodel.sql.sqltypes.AutoString(length=20),
            nullable=False,
            server_default="member",
        ),
    )
    # Copy existing is_superuser=true users to role='admin'
    op.execute("UPDATE \"user\" SET role = 'admin' WHERE is_superuser = TRUE")
    # Remove the old is_superuser column
    op.drop_column("user", "is_superuser")


def downgrade() -> None:
    # Add back the is_superuser column
    op.add_column(
        "user",
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )
    # Copy role='admin' back to is_superuser=true
    op.execute("UPDATE \"user\" SET is_superuser = TRUE WHERE role = 'admin'")
    # Remove the role column
    op.drop_column("user", "role")
