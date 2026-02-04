import getpass

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.core.permissions import PERMISSIONS

from app.modules.users.models import User
from app.modules.roles.models import Role, UserRole, RolePermission


def seed_initial_data(db: Session):
    
    user_exists = db.query(User).first()
    if user_exists:
        return

    print("\n First time setup — create SUPERADMIN user\n")

    email = input("Admin email: ")
    password = getpass.getpass("Password: ")

    role = Role(name="superadmin")
    db.add(role)
    db.flush()

    for perm in PERMISSIONS:
        db.add(RolePermission(role_id=role.id, permission_code=perm))

    user = User(
        email=email,
        password_hash=hash_password(password),
        is_active=True,
    )
    db.add(user)
    db.flush()

    db.add(UserRole(user_id=user.id, role_id=role.id))

    db.commit()

    print("\nSuperadmin created successfully!\n")
