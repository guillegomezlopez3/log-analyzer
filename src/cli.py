"""Command line interface.

Usage: python -m src.cli access.log --top 5
"""
import argparse
import time

from .analyzer import analyze_file


def main() -> None:
    p = argparse.ArgumentParser(description="Analyze a web server access log")
    p.add_argument("logfile")
    p.add_argument("--top", type=int, default=5)
    a = p.parse_args()

    start = time.perf_counter()
    s = analyze_file(a.logfile)
    elapsed = time.perf_counter() - start

    print(f"Requests: {s.total:,} (malformed: {s.malformed:,}) in {elapsed:.2f}s "
          f"({s.total / max(elapsed, 1e-9):,.0f} lines/s)")
    print(f"Data sent: {s.bytes_sent / 1e6:,.1f} MB | 5xx error rate: {s.error_rate:.2%}")
    print("\nStatus classes:", dict(sorted(s.by_status_class.items())))
    print(f"\nTop {a.top} paths:")
    for path, n in s.by_path.most_common(a.top):
        print(f"  {n:>9,}  {path}")
    print(f"\nTop {a.top} client IPs:")
    for ip, n in s.by_ip.most_common(a.top):
        print(f"  {n:>9,}  {ip}")
    if s.errors_by_path:
        print("\nPaths with most 5xx errors:")
        for path, n in s.errors_by_path.most_common(a.top):
            print(f"  {n:>9,}  {path}")


if __name__ == "__main__":
    main()
