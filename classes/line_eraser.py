import sys


def erase_lines(n=1):
    for _ in range(n):
        sys.stdout.write('\x1b[1A')  # Move cursor up by 1 line
        sys.stdout.write('\x1b[2K')  # Clear entire line
    sys.stdout.flush()
