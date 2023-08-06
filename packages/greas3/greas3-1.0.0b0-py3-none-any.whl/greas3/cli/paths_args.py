from dataclasses import dataclass

from boto3.session import Session


@dataclass
class PathsArgs:
    source: str
    destination: str
    dry_run: bool
    session: Session
