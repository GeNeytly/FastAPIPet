from fastapi import APIRouter

from users.schemas import SCreateUser
from users.crud import get_create_user

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/")
def create_user(user: SCreateUser):
    user = get_create_user(user_in=user)
    return user
