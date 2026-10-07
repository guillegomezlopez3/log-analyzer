"""Parsing of Common Log Format lines."""
import re
from dataclasses import dataclass
from datetime import datetime

LINE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>[A-Z]+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\d+|-)$')


@dataclass(frozen=True)
class Entry:
    ip: str
    time: datetime
    method: str
    path: str
    status: int
    size: int


def parse_line(line: str) -> Entry | None:
    """Return an Entry, or None if the line is malformed."""
    m = LINE.match(line.strip())
    if not m:
        return None
    try:
        t = datetime.strptime(m["time"], "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        return None
    size = 0 if m["size"] == "-" else int(m["size"])
    return Entry(m["ip"], t, m["method"], m["path"], int(m["status"]), size)
