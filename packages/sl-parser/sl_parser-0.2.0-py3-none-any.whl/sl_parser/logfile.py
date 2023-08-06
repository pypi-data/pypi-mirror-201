import csv
import re
from datetime import datetime

from pydantic import BaseModel

from .logentry import LogEntry
from .unit import Unit

HEADER_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
INI_FILENAME_PREFIX = "INI File name :  "
UNIT_SUBUNIT_RE = re.compile(r"^Unit=(\d+) - SubUnit=(\d+)$")


class LogFile(BaseModel):
    filename: str
    pc_datetime: datetime
    ups_datetime: datetime
    units_subunits: dict[int, Unit]
    log_entries: list[LogEntry]

    class Config:
        json_encoders = {
            "datetime": lambda v: v.timedelta_isoformat(),
        }

    @staticmethod
    def parse_log(filename: str, log: str) -> "LogFile":
        log_lines = log.splitlines()
        pc_datetime = datetime.strptime(log_lines.pop(0).split(": ")[1], HEADER_DATETIME_FORMAT)
        ups_datetime = datetime.strptime(log_lines.pop(0).split(": ")[1], HEADER_DATETIME_FORMAT)
        units_subunits: dict[int, Unit] = {}

        while log_lines[0].startswith(INI_FILENAME_PREFIX):
            ini_line = log_lines.pop(0)
            ini_file, unit_subunit_str = ini_line.removeprefix(INI_FILENAME_PREFIX).split(";")
            unit, subunit = (
                int(i) for i in UNIT_SUBUNIT_RE.fullmatch(unit_subunit_str.strip()).groups()  # type: ignore
            )
            if subunit == 0:
                units_subunits[unit] = Unit(ini_file=ini_file)
            units_subunits[unit].subunits[subunit] = ini_file

        log_lines.pop(0)  # remove column headers
        log_entries = [
            LogEntry.parse_from_csv_row([r.strip() for r in row], units_subunits)
            for row in csv.reader(log_lines, delimiter=";")
            if row[0].strip() != "01/01/0001"
            and row[1].strip() != "00:00:00.000"  # some logs contain "empty" rows with this timestamp
        ]

        return LogFile(
            pc_datetime=pc_datetime,
            ups_datetime=ups_datetime,
            units_subunits=units_subunits,
            log_entries=log_entries,
            filename=filename,
        )
