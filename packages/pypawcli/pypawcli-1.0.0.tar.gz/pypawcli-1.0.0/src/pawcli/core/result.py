from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

from pawapi import Response
from typer import Exit

from .formatter import JsonFormatter

Content = Union[Union[Dict[str, Any], Sequence[Any]], bytes]


def check_status_code(
    status: int,
    expected: Union[int, List[int]] = 200,
) -> None:  # pragma: no cover
    if not isinstance(expected, list):
        expected = [expected]
    if status not in expected:
        print(f"Expected status is {expected!r}, got {status}")
        raise Exit(1)


def process_result(
    response: Response,
    *,
    expected_status: Union[int, List[int]] = 200,
    print_content: bool = True,
    formatter: Optional[Callable[[Content], str]] = None,
    callback: Optional[Callable[[Content], None]] = None,
) -> None:  # pragma: no cover
    check_status_code(response.status, expected_status)
    if response.content:
        if print_content:
            if formatter is None:
                formatter = JsonFormatter()
            print(formatter(response.content))
        if callback is not None:
            callback(response.content)
