from datetime import datetime

from pydantic import BaseModel
from pydantic_computed import computed

from .unit import Unit

LOG_ENTRY_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S.%f"


class LogEntry(BaseModel):
    timestamp: datetime
    unit: int
    subunit: int
    unit_subunit_id: int
    ini_filename: str
    code: str
    description: str
    value: str
    type_um: str
    snapshot: str
    color: str

    class Config:
        json_encoders = {
            "datetime": lambda v: v.timedelta_isoformat(),
        }

    @computed("unit_subunit_id")  # type: ignore
    def __calculate_unit_subunit_id(unit: int, subunit: int, **kwargs) -> int:  # type: ignore  # noqa: N805, ANN003
        return (unit << 4) | subunit

    @staticmethod
    def parse_from_csv_row(csv_row: list[str], units_subunits: dict[int, Unit]) -> "LogEntry":
        timestamp = datetime.strptime(f"{csv_row[0]} {csv_row[1]}000", LOG_ENTRY_DATETIME_FORMAT)
        return LogEntry(
            timestamp=timestamp,
            unit=int(csv_row[2]),
            subunit=int(csv_row[3]),
            # workaround for pydantic validation error if constructor is called without unit_subunit_id
            unit_subunit_id=-1,
            ini_filename=units_subunits[int(csv_row[2])].subunits[int(csv_row[3])],
            code=csv_row[4],
            description=csv_row[5],
            value=csv_row[6],
            type_um=csv_row[7],
            snapshot=csv_row[8],
            color=csv_row[9],
        )  # type: ignore
