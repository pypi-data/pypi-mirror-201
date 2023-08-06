from pydantic import BaseModel


class Unit(BaseModel):
    ini_file: str
    subunits: dict[int, str] = {}
