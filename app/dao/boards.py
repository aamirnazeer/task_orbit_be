from sqlalchemy.orm import Session
from app.models.boards import Boards


class BoardsDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_new_board(self, boards: Boards):
        self.db.add(boards)
        self.db.commit()
        self.db.refresh(boards)
        return boards
