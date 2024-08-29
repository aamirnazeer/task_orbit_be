from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.refresh_tokens import RefreshTokens


class RefreshTokensDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_new_refresh_token(self, token: RefreshTokens):
        self.db.add(token)
        self.db.commit()

    def get_refresh_token(self, token: str):
        token = self.db.query(RefreshTokens).filter(RefreshTokens.token == token).first()
        return token

    def delete_token(self, user_id):
        stmt = delete(RefreshTokens).where(RefreshTokens.user_id == user_id)
        self.db.execute(stmt)
        self.db.commit()
