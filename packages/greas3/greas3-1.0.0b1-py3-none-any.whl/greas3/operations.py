from pathlib import Path
from typing import List, Optional, Union

from ansiscape import green, heavy, yellow
from boto3.session import Session
from slash3 import S3Uri

from greas3.logging import logger
from greas3.put_operation import PutOperation
from greas3.put_operations import PutOperations


def put(
    path: Union[Path, str],
    uri: Union[S3Uri, str],
    dry_run: bool = False,
    session: Optional[Session] = None,
) -> List[PutOperation]:
    """
    Uploads a local file or directory to S3 if they're new or different.

    Returns a list of every upload operation. Each operation indicates whether
    or not an upload was warranted.

    `dry_run` will discover the required operations but will not perform them.

    `session` is an optional Boto3 session. A new session will be created if
    omitted.
    """

    path = Path(path) if isinstance(path, str) else path
    uri = S3Uri(uri) if isinstance(uri, str) else uri

    if path.is_dir():
        operations = PutOperations.from_dir(path, uri)
        path_title = path.as_posix()
        uri_title = uri.uri
    else:
        operations = PutOperations.from_file(path, uri)
        path_title = path.parent.as_posix()
        if uri.uri.endswith("/"):
            uri_title = uri.uri
        else:
            uri_title = uri.parent.uri

    path_len = max(operations.longest_relative_path, len(path_title))

    logger.info(
        "%s   %s",
        heavy(path_title.ljust(path_len)),
        heavy(uri_title),
    )

    session = session or Session()
    s3 = session.client("s3")

    ordered_operations = operations.operations

    for op in operations.operations:
        same = op.are_same(session)

        logger.info(
            "%s %s %s",
            op.relative_path.ljust(path_len),
            green("=") if same else yellow(">"),
            op.relative_uri,
        )

        if same or dry_run:
            continue

        s3.upload_file(
            Bucket=op.uri.bucket,
            ExtraArgs={"ChecksumAlgorithm": "SHA256"},
            Filename=op.path.as_posix(),
            Key=op.uri.key.key,
        )

    return ordered_operations
