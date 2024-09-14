from pydantic import BaseModel, Field


class CreateNewBoard(BaseModel):
    board_name: str = Field(min_length=3)

    model_config = {
        "json_schema_extra": {
            "example": {
                "board_name": "new board",
            }
        }
    }
