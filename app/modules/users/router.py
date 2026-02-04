from fastapi import APIRouter, Depends

from app.dependencies import get_db
from app.core.permissions import require_permission

from .schemas import UserCreate, UserUpdate, UserResponse
from .service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


def get_service(db=Depends(get_db)):
    return UserService(db)


@router.get("", response_model=list[UserResponse])
def list_users(
    user=Depends(require_permission("user.read")),
    service: UserService = Depends(get_service),
):
    return service.list_users()


@router.post("", response_model=UserResponse)
def create_user(
    data: UserCreate,
    user=Depends(require_permission("user.create")),
    service: UserService = Depends(get_service),
):
    return service.create_user(data.email, data.password)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    user=Depends(require_permission("user.read")),
    service: UserService = Depends(get_service),
):
    return service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    user=Depends(require_permission("user.update")),
    service: UserService = Depends(get_service),
):
    return service.update_user(user_id, **data.dict(exclude_unset=True))


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user=Depends(require_permission("user.delete")),
    service: UserService = Depends(get_service),
):
    service.delete_user(user_id)
    return {"message": "user disabled"}
