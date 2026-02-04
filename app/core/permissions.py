from fastapi import Request, HTTPException

PERMISSIONS = {
    # for user management
    "user.create",
    "user.read",
    "user.update",
    "user.delete",

    # fore role management
    "role.manage",

    # for inventory management
    "inventory.read",
    "inventory.adjust",
    "inventory.transfer",

    # for orders management
    "order.create",
    "order.complete",
    "order.cancel",

    # for reports management
    "reports.read",
}


def require_permission(code: str):
    def dependency(request: Request):
        user = getattr(request.state, "user", None)

        if not user:
            raise HTTPException(401, "Not authenticated")

        permissions = getattr(request.state, "permissions", set())

        if code not in permissions:
            raise HTTPException(403, "Forbidden")

        return user

    return dependency
