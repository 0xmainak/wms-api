from fastapi import APIRouter, Depends

from app.dependencies import get_db, require_user
from app.core.permissions import require_permission

from .schemas import RoleCreate, RoleUpdate, RoleResponse, PermissionAssign
from .service import RoleService


router = APIRouter(prefix="/roles", tags=["Roles"])


def get_service(db=Depends(get_db)):
    return RoleService(db)


@router.get("", response_model=list[RoleResponse])
def list_roles(user=Depends(require_user), service: RoleService = Depends(get_service)):
    return service.list_roles()


@router.post("", response_model=RoleResponse)
def create_role(data: RoleCreate,
                user=Depends(require_permission("role.manage")),
                service: RoleService = Depends(get_service)):
    return service.create_role(data.name)


@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, data: RoleUpdate,
                user=Depends(require_permission("role.manage")),
                service: RoleService = Depends(get_service)):
    return service.update_role(role_id, data.name)


@router.delete("/{role_id}")
def delete_role(role_id: int,
                user=Depends(require_permission("role.manage")),
                service: RoleService = Depends(get_service)):
    service.delete_role(role_id)
    return {"message": "deleted"}


@router.get("/{role_id}/permissions")
def list_permissions(role_id: int, user=Depends(require_user), service: RoleService = Depends(get_service)):
    return service.list_permissions(role_id)


@router.post("/{role_id}/permissions")
def add_permission(role_id: int, data: PermissionAssign,
                   user=Depends(require_permission("role.manage")),
                   service: RoleService = Depends(get_service)):
    service.assign_permission(role_id, data.code)
    return {"message": "added"}


@router.delete("/{role_id}/permissions/{code}")
def remove_permission(role_id: int, code: str,
                      user=Depends(require_permission("role.manage")),
                      service: RoleService = Depends(get_service)):
    service.remove_permission(role_id, code)
    return {"message": "removed"}
