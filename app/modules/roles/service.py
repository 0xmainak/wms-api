from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.permissions import PERMISSIONS

from .repository import RoleRepository
from .models import Role


class RoleService:
    def __init__(self, db: Session):
        self.repo = RoleRepository(db)

    def list_roles(self):
        return self.repo.list_roles()

    def create_role(self, name: str):
        role = Role(name=name)
        return self.repo.create(role)

    def update_role(self, role_id: int, name: str):
        role = self.repo.get(role_id)
        if not role:
            raise HTTPException(404, "Role not found")

        role.name = name
        self.repo.commit()
        return role

    def delete_role(self, role_id: int):
        role = self.repo.get(role_id)
        if not role:
            raise HTTPException(404, "Role not found")

        self.repo.db.delete(role)
        self.repo.commit()

    def assign_permission(self, role_id: int, code: str):
        if code not in PERMISSIONS:
            raise HTTPException(400, "Invalid permission")

        self.repo.add_permission(role_id, code)

    def remove_permission(self, role_id: int, code: str):
        self.repo.remove_permission(role_id, code)

    def list_permissions(self, role_id: int):
        return self.repo.get_permissions(role_id)

    def assign_role_to_user(self, user_id: int, role_id: int):
        self.repo.add_user_role(user_id, role_id)

    def remove_role_from_user(self, user_id: int, role_id: int):
        self.repo.remove_user_role(user_id, role_id)
