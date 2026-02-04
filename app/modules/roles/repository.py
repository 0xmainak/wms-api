from sqlalchemy.orm import Session

from .models import Role, UserRole, RolePermission


class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_roles(self):
        return self.db.query(Role).all()

    def get(self, role_id: int):
        return self.db.get(Role, role_id)

    def create(self, role: Role):
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def commit(self):
        self.db.commit()

    def add_permission(self, role_id: int, code: str):
        self.db.add(RolePermission(role_id=role_id, permission_code=code))
        self.db.commit()

    def remove_permission(self, role_id: int, code: str):
        self.db.query(RolePermission).filter_by(
            role_id=role_id,
            permission_code=code,
        ).delete()
        self.db.commit()

    def get_permissions(self, role_id: int):
        rows = self.db.query(RolePermission).filter_by(role_id=role_id).all()
        return [r.permission_code for r in rows]

    def add_user_role(self, user_id: int, role_id: int):
        self.db.add(UserRole(user_id=user_id, role_id=role_id))
        self.db.commit()

    def remove_user_role(self, user_id: int, role_id: int):
        self.db.query(UserRole).filter_by(
            user_id=user_id,
            role_id=role_id,
        ).delete()
        self.db.commit()

    def get_user_roles(self, user_id: int):
        return self.db.query(UserRole).filter_by(user_id=user_id).all()
