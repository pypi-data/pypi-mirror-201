from pydantic import BaseModel, validator, Field


# класс для входных данных о товарах
class Entry(BaseModel):
    id: int = Field(
        default=0,
        title="The idgood of item.",
        description="Needs to be an integer positive number.",
        example=10004,
    )
    cnt: int = Field(
        default=0,
        title="The quantity of items.",
        description="Needs to be an integer positive number.",
        example=2,
    )

    @validator("id")
    def check_id(cls, v):
        if v < 1:
            raise ValueError("id must be > 0")
        return v

    @validator("cnt")
    def check_cnt(cls, v):
        if v < 0:
            raise ValueError("cnt must be >= 0")
        return v


# класс для входных данных о товарах с возможностью возврата изначальных размеров
class ComplEntry(BaseModel):
    items: list[Entry] = []
    return_sizes_goods: bool = Field(
        default=False,
        title="True if you need to see the initial sizes of all items which ids you wrote in 'id' fields.",
        description="Can only be True or False.",
    )

    class Config:
        schema_extra = {
            "example": {"items": [{"id": 10004, "cnt": 2}], "return_sizes_goods": True}
        }

    @validator("items")
    def check_items(cls, v):
        if v is None:
            raise ValueError("Entry is empty")
        if len(v) == 0:
            raise ValueError("No items entered")
        return v
