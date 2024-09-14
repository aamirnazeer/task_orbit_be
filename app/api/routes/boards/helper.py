from app.models.boards import Boards


def create_new_board(body, current_user_id):
    board_model = Boards(board_name=body.board_name, board_owner=current_user_id)
    return board_model
