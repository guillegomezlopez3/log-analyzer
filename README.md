# log-analyzer

Streaming analyzer for web server access logs (Common Log Format), written in pure Python. It reads the file **line by line in a single pass with constant memory**, so the same code works on a 1 MB log or a multi-GB one.

## What it reports

- Total requests, malformed lines, bytes sent
- Distribution by status class (2xx / 3xx / 4xx / 5xx) and the 5xx error rate
- Top paths and top client IPs
- Paths that produce the most server errors
- Requests per hour (collected in `Stats.by_hour`)
- Processing speed in lines per second

## Stack

Python 3.11+ · standard library only (`re`, `collections`, `dataclasses`) · pytest

## Run

```bash
python -m src.generate_logs --lines 1000000 --out access.log   # synthetic test data
python -m src.cli access.log --top 5
pytest
```

Example output (1M generated lines):

```
Requests: 1,000,000 (malformed: 0)
Data sent: 25,089.8 MB | 5xx error rate: 1.99%
Status classes: {'2xx': 829844, '3xx': 69828, '4xx': 80420, '5xx': 19908}
```

## Design

- `parser.py`: regex-based parser that returns a typed `Entry` or `None` for malformed lines, never an exception.
- `analyzer.py`: accumulates `Counter` objects while iterating, so memory depends on the number of distinct paths and IPs, not on file size.
- `cli.py`: command line front-end.

## Ideas for next steps

Parallel processing by file chunks, rolling time windows for anomaly detection, and export of the stats to JSON or CSV.
