#!/usr/bin/python3
import sys
import signal

total_size = 0
status_counts = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

def print_statistics(total_size, status_counts):
    print(f"File size: {total_size}")
    for status in sorted(status_counts.keys()):
        if status_counts[status] > 0:
            print(f"{status}: {status_counts[status]}")

def parse_line(line):
    parts = line.split()
    if len(parts) < 9:
        return None
    ip_address = parts[0]
    date = parts[3][1:]
    method = parts[5][1:]
    resource = parts[6]
    protocol = parts[7][:-1]
    try:
        status_code = int(parts[8])
        file_size = int(parts[9])
    except ValueError:
        return None

    if method == "GET" and resource == "/projects/260" and protocol == "HTTP/1.1":
        return status_code, file_size
    return None

def signal_handler(sig, frame):
    print_statistics(total_size, status_counts)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        line_count += 1
        result = parse_line(line.strip())
        if result:
            status_code, file_size = result
            total_size += file_size
            if status_code in status_counts:
                status_counts[status_code] += 1

        if line_count % 10 == 0:
            print_statistics(total_size, status_counts)

except KeyboardInterrupt:
    print_statistics(total_size, status_counts)
    sys.exit(0)