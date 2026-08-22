#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys


def run(program: str, line: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([program, line], text=True, capture_output=True, check=False)


def main() -> int:
    if len(sys.argv) != 2:
        print("runner path required", file=sys.stderr)
        return 2
    runner = sys.argv[1]
    result = run(runner, "alpha 'two three' \"\" left\\ right | omega")
    expected = (
        "command[0].argv[0]=<alpha>\n"
        "command[0].argv[1]=<two three>\n"
        "command[0].argv[2]=<>\n"
        "command[0].argv[3]=<left right>\n"
        "command[1].argv[0]=<omega>\n"
    )
    if result.returncode != 0 or result.stdout != expected or result.stderr:
        raise AssertionError((result.returncode, result.stdout, result.stderr))
    for line in ("", "| x", "x |", "x | y | z", "'unterminated", "x > file"):
        result = run(runner, line)
        if result.returncode != 2 or "Syntax error:" not in result.stderr:
            raise AssertionError((line, result.returncode, result.stderr))
    print("command-runner parser tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
