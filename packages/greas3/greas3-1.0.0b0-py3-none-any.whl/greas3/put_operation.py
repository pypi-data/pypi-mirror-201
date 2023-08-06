from pathlib import Path
from typing import Any, Optional

from boto3.session import Session
from slash3 import S3Uri

from greas3.check import are_same


class PutOperation:
    """
    An upload operation.

    `path` describes the local source path.

    `uri` describes the destination S3 URI.

    `relative_path` and `relative_uri` describe the relative paths from the root
    directory and URI, and are used only for logging.
    """

    def __init__(
        self,
        path: Path,
        relative_path: str,
        uri: S3Uri,
        relative_uri: str,
    ) -> None:
        self._same: Optional[bool] = None
        self.path = path
        self.relative_path = relative_path
        self.uri = uri
        self.relative_uri = relative_uri

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, PutOperation)
            and self.path == other.path
            and self.relative_path == other.relative_path
            and self.uri == other.uri
            and self.relative_uri == other.relative_uri
        )

    def are_same(self, session: Optional[Session] = None) -> bool:
        """
        Determines whether or not the local and remote file are the same.
        """

        if self._same is None:
            session = session or Session()
            self._same = are_same(self.path, self.uri, session)
        return self._same
