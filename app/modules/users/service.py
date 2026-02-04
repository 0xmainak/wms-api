from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password

from .repository import UserRepository
from .models import User


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def list_users(self):
        return self.repo.list()

    def get_user(self, user_id: int):
        user = self.repo.get(user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user

    def create_user(self, email: str, password: str):
        if self.repo.get_by_email(email):
            raise HTTPException(400, "Email already exists")

        user = User(
            email=email,
            password_hash=hash_password(password),
            is_active=True,
        )

        return self.repo.create(user)

    def update_user(self, user_id: int, **fields):
        user = self.get_user(user_id)

        if fields.get("email"):
            user.email = fields["email"]

        if fields.get("password"):
            user.password_hash = hash_password(fields["password"])

        if fields.get("is_active") is not None:
            user.is_active = fields["is_active"]

        self.repo.commit()
        return user

    def delete_user(self, user_id: int):
        user = self.get_user(user_id)
        user.is_active = False
        self.repo.commit()
