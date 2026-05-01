from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate, UserRole

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    # Seed admin user from environment config
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role=UserRole.ADMIN,
        )
        user = crud.create_user(session=session, user_create=user_in)

    # Seed a manager user for development / testing
    manager_email = "manager@example.com"
    manager = session.exec(
        select(User).where(User.email == manager_email)
    ).first()
    if not manager:
        user_in = UserCreate(
            email=manager_email,
            password="admin123",  # Valid: >= 8 chars
            role=UserRole.MANAGER,
        )
        manager = crud.create_user(session=session, user_create=user_in)

    # Seed a regular member user for development / testing
    member_email = "member@example.com"
    member = session.exec(
        select(User).where(User.email == member_email)
    ).first()
    if not member:
        user_in = UserCreate(
            email=member_email,
            password="member123",  # Valid: >= 8 chars
            role=UserRole.MEMBER,
        )
        member = crud.create_user(session=session, user_create=user_in)
