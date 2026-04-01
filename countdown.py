#!/usr/bin/env python3
import sys
import time
import argparse


def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def countdown(seconds, label=""):
    total = seconds
    try:
        while seconds >= 0:
            display = format_time(seconds)
            suffix = f"  {label}" if label else ""
            print(f"\r{display}{suffix}  ", end="", flush=True)
            if seconds == 0:
                break
            time.sleep(1)
            seconds -= 1
        print("\n\a Done!")  # \a rings the terminal bell
    except KeyboardInterrupt:
        remaining = format_time(seconds)
        print(f"\n Stopped with {remaining} remaining.")
        sys.exit(0)


def parse_time(value):
    """Accept formats: 90 (seconds), 1:30 (mm:ss), 1:30:00 (hh:mm:ss), or 5m, 2h30m."""
    value = value.strip()

    # Handle shorthand like 5m, 2h, 1h30m, 90s
    if any(c in value for c in "hms"):
        import re
        total = 0
        for amount, unit in re.findall(r"(\d+)\s*([hms])", value):
            amount = int(amount)
            if unit == "h":
                total += amount * 3600
            elif unit == "m":
                total += amount * 60
            elif unit == "s":
                total += amount
        return total

    # Handle HH:MM:SS or MM:SS
    parts = value.split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])

    # Plain seconds
    return int(value)


def main():
    parser = argparse.ArgumentParser(
        description="Countdown timer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 90            # 90 seconds
  %(prog)s 5m            # 5 minutes
  %(prog)s 1h30m         # 1 hour 30 minutes
  %(prog)s 2:30          # 2 minutes 30 seconds
  %(prog)s 5m "Pomodoro" # with a label
        """,
    )
    parser.add_argument("duration", help="Duration (e.g. 90, 5m, 1h30m, 2:30)")
    parser.add_argument("label", nargs="?", default="", help="Optional label")
    args = parser.parse_args()

    try:
        seconds = parse_time(args.duration)
    except (ValueError, AttributeError):
        print(f"Error: could not parse duration '{args.duration}'")
        sys.exit(1)

    if seconds <= 0:
        print("Duration must be greater than 0.")
        sys.exit(1)

    print(f"Starting {format_time(seconds)} countdown{'  ' + args.label if args.label else ''}...")
    countdown(seconds, args.label)


if __name__ == "__main__":
    main()
