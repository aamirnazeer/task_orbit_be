from app.api.routes.boards import helper as boards_helper
from app.api.common.utils import read_token
from app.dao.boards import BoardsDAO


def create_new_board(db, body, current_user):
    board_model = boards_helper.create_new_board(body, current_user.get("id"))

    _boards = BoardsDAO(db)
    board = _boards.create_new_board(board_model)
    return {"board_name": board.board_name, "uuid": board.uuid}
