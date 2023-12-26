from users.schemas import SCreateUser


def get_create_user(user_in: SCreateUser):
    user = user_in.model_dump()
    return {'status': 'ok', 'user': user}
