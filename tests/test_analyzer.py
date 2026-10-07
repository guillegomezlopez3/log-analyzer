from src.analyzer import analyze
from src.generate_logs import generate
from src.parser import parse_line

GOOD = '10.0.0.1 - - [01/Mar/2026:10:15:00 +0000] "GET /api/users HTTP/1.1" 200 512'


def test_parse_valid_line():
    e = parse_line(GOOD)
    assert (e.ip, e.method, e.path, e.status, e.size) == ("10.0.0.1", "GET", "/api/users", 200, 512)
    assert e.time.hour == 10


def test_parse_dash_size_and_malformed():
    assert parse_line(GOOD.replace("512", "-")).size == 0
    assert parse_line("garbage line") is None
    assert parse_line(GOOD.replace("01/Mar", "99/Foo")) is None


def test_analyze_counts():
    lines = [GOOD, GOOD.replace("200", "500"), GOOD.replace("/api/users", "/login"), "bad", ""]
    s = analyze(lines)
    assert s.total == 3 and s.malformed == 1
    assert s.by_status_class["2xx"] == 2 and s.by_status_class["5xx"] == 1
    assert s.by_path.most_common(1)[0] == ("/api/users", 2)
    assert s.error_rate == 1 / 3


def test_generated_logs_are_all_parseable():
    s = analyze(generate(2000))
    assert s.total == 2000 and s.malformed == 0
