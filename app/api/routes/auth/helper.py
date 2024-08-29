from app.api.common.dependencies import bcrypt_context
from app.models.refresh_tokens import RefreshTokens
from app.models.users import Users


def create_new_user(body):
    user_model = Users(
        phone_number=body.first_name,
        first_name=body.first_name,
        last_name=body.last_name,
        role=body.role,
        email=body.email,
        username=body.username,
        hashed_password=bcrypt_context.hash(body.password)
    )
    return user_model


def create_new_refresh_token(token, user_id):
    token_model = RefreshTokens(token=token, user_id=user_id)
    return token_model
