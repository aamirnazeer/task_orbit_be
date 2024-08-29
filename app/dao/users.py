from sqlalchemy.orm import Session
from app.models.users import Users


class UsersDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_new_user(self, user: Users):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_user(self, username: str):
        user = self.db.query(Users).filter(Users.username == username).first()
        return user
