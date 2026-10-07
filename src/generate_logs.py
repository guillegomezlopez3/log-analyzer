"""Generate a synthetic web-server access log (Common Log Format) for testing.

Usage: python -m src.generate_logs --lines 1000000 --out access.log
"""
import argparse
import random
from datetime import datetime, timedelta

PATHS = ["/", "/login", "/api/users", "/api/orders", "/api/products", "/static/app.js", "/static/style.css", "/admin", "/health"]
STATUS = [200] * 80 + [201] * 3 + [301] * 3 + [304] * 4 + [400] * 2 + [401] * 2 + [403] + [404] * 3 + [500] * 1 + [503]
METHODS = ["GET"] * 8 + ["POST"] * 2


def generate(lines: int, seed: int = 1):
    rnd = random.Random(seed)
    ips = [f"192.168.{rnd.randint(0, 20)}.{rnd.randint(1, 254)}" for _ in range(300)]
    t = datetime(2026, 3, 1)
    for _ in range(lines):
        t += timedelta(seconds=rnd.random() * 2)
        yield (f'{rnd.choice(ips)} - - [{t:%d/%b/%Y:%H:%M:%S} +0000] '
               f'"{rnd.choice(METHODS)} {rnd.choice(PATHS)} HTTP/1.1" {rnd.choice(STATUS)} {rnd.randint(200, 50000)}')


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--lines", type=int, default=100_000)
    p.add_argument("--out", default="access.log")
    a = p.parse_args()
    with open(a.out, "w") as f:
        for line in generate(a.lines):
            f.write(line + "\n")
    print(f"Wrote {a.lines} lines to {a.out}")


if __name__ == "__main__":
    main()
