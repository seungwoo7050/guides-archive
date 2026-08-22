#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, subprocess
from pathlib import Path

def execute(path: Path, *args: str, timeout: float = 10.0) -> str:
    result=subprocess.run([str(path),*args],text=True,capture_output=True,timeout=timeout,check=False)
    if result.returncode != 0:
        raise AssertionError(f"{path.name} failed: {result.returncode}: {result.stderr}")
    return result.stdout

def require(text: str, pattern: str) -> None:
    if re.search(pattern,text,re.MULTILINE) is None: raise AssertionError(f"missing {pattern!r} in {text!r}")

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument('--build-dir',required=True); args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]; build=(root/'examples'/args.build_dir).resolve()
    require(execute(build/'syscall-boundary'),r'write 호출.*\n.*errno=2')
    require(execute(build/'lost-update','split','100'),r'mode=split rounds=100 expected=200 actual=100')
    require(execute(build/'lost-update','fetch-add','100'),r'mode=fetch-add rounds=100 expected=200 actual=200')
    require(execute(build/'bounded-buffer','100'),r'produced=100 consumed=100 sums_match=yes')
    require(execute(build/'dining-cycle','50'),r'diners=5 rounds=50 all_completed=yes lock_order=lower-first')
    require(execute(build/'cow-observer'),r'parent .* value=41 unchanged=yes')
    require(execute(build/'page-fault-observer','32'),r'touched_pages=32 .*minor_fault_delta=\d+')
    for program,bad in [('lost-update','bad'),('bounded-buffer','0'),('dining-cycle','0'),('page-fault-observer','0')]:
        result=subprocess.run([str(build/program),bad],capture_output=True,timeout=5,check=False)
        if result.returncode != 2: raise AssertionError(f'{program} accepted invalid input')
    print('Operating-system examples verified.')
    return 0
if __name__=='__main__': raise SystemExit(main())
