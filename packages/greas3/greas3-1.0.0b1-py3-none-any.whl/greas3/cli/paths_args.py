from dataclasses import dataclass
from typing import Optional

from boto3.session import Session


@dataclass
class PathsArgs:
    destination: str
    source: str

    debug: bool = False
    dry_run: bool = False
    session: Optional[Session] = None
