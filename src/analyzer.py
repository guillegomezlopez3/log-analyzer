"""Streaming log analysis: constant memory, one pass over the file."""
from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable

from .parser import parse_line


@dataclass
class Stats:
    total: int = 0
    malformed: int = 0
    bytes_sent: int = 0
    by_status_class: Counter = field(default_factory=Counter)
    by_path: Counter = field(default_factory=Counter)
    by_ip: Counter = field(default_factory=Counter)
    errors_by_path: Counter = field(default_factory=Counter)
    by_hour: Counter = field(default_factory=Counter)

    @property
    def error_rate(self) -> float:
        errors = self.by_status_class["5xx"]
        return errors / self.total if self.total else 0.0


def analyze(lines: Iterable[str]) -> Stats:
    s = Stats()
    for line in lines:
        if not line.strip():
            continue
        e = parse_line(line)
        if e is None:
            s.malformed += 1
            continue
        s.total += 1
        s.bytes_sent += e.size
        s.by_status_class[f"{e.status // 100}xx"] += 1
        s.by_path[e.path] += 1
        s.by_ip[e.ip] += 1
        s.by_hour[e.time.strftime("%Y-%m-%d %H:00")] += 1
        if e.status >= 500:
            s.errors_by_path[e.path] += 1
    return s


def analyze_file(path: str) -> Stats:
    with open(path, encoding="utf-8", errors="replace") as f:
        return analyze(f)
