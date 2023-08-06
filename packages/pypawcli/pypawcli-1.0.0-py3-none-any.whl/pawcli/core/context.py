from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Optional

from pawapi import Region

if TYPE_CHECKING:  # pragma: no cover
    from pawapi import Pawapi

    from .config import Config


@dataclass
class Credentials:  # pragma: no cover
    username: Optional[str] = None
    token: Optional[str] = None
    region: Region = Region.US


@dataclass
class ContextObject:  # pragma: no cover
    config: Config
    credentials: Credentials
    api: Optional[Pawapi] = None
