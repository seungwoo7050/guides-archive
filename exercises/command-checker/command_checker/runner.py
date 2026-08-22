"""실행 파일을 선택하고 사례 실행과 결과 출력을 처리합니다."""

from __future__ import annotations

import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Sequence, TextIO

from .model import Case, ExecutionError, Result, SpecificationError
from .process import run_case


# [Implementation 5] Resolve the target executable once before running cases.
def validate_executable(command: str) -> str:
    contains_separator = os.sep in command or (os.altsep is not None and os.altsep in command)
    if contains_separator:
        path = Path(command).resolve()
    else:
        selected = shutil.which(command)
        if selected is None:
            raise SpecificationError(f"command not found on PATH: {command}")
        path = Path(selected).resolve()
    if not path.is_file() or not os.access(path, os.X_OK):
        raise SpecificationError(f"command is not executable: {command}")
    return str(path)


# [Implementation 6] Run cases sequentially and preserve input order.
def run_cases(
    cases: Sequence[Case],
    command: Sequence[str],
    jobs: int,
) -> tuple[Result, ...]:
    if jobs < 1:
        raise SpecificationError("jobs must be at least 1")
    if jobs == 1:
        return tuple(run_case(case, command) for case in cases)
