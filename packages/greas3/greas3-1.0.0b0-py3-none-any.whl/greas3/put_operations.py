from os import walk
from pathlib import Path
from typing import List

from slash3 import S3Uri

from greas3.logging import logger
from greas3.put_operation import PutOperation


class PutOperations:
    """
    A collection of local paths and remote URIs to upload to.

    `root_dir` is the root directory from which local files will be uploaded.
    For example, if files and/or subdirectories will be uploaded from
    "/home/cariad/" then pass "/home/cariad/".

    `root_uri` is the root S3 URI to which files will be uploaded. For example,
    if files will and/or subdirectories will be uploaded to "s3://circus/new/"
    then pass "s3://circus/new/".
    """

    def __init__(
        self,
        root_dir: Path,
        root_uri: S3Uri,
    ) -> None:
        self._operations: List[PutOperation] = []

        self.longest_relative_path = 0
        """
        The length of the longest relative local path encountered so far.
        """

        self.root_dir = root_dir
        """
        The root directory from which local files will be uploaded.
        """

        self.root_uri = root_uri
        """
        The root S3 URI to which files will be uploaded.
        """

    def add(self, path: Path, uri: S3Uri) -> None:
        """
        Adds a local file and its destination URI to the collection.
        """

        logger.debug("Adding an operation to put file %s to %s", path, uri)

        rel_path = path.relative_to(self.root_dir).as_posix()
        rel_uri = uri.relative_to(self.root_uri)

        self.longest_relative_path = max(
            self.longest_relative_path,
            len(rel_path),
        )

        self._operations.append(PutOperation(path, rel_path, uri, rel_uri))

    @classmethod
    def from_dir(cls, directory: Path, root_uri: S3Uri) -> "PutOperations":
        """
        Constructs a collection of operations to upload every file in every
        subdirectory of `directory`.

        Key prefixes will be added to `root_uri` to reflect the local directory
        structure.
        """

        operations = PutOperations(directory, root_uri)

        for dir, _, filenames in walk(directory):
            dir_path = Path(dir)
            uri = root_uri

            for part in dir_path.relative_to(directory).parts:
                uri /= part

            for filename in filenames:
                operations.add(dir_path / filename, uri / filename)

        return operations

    @classmethod
    def from_file(cls, path: Path, uri: S3Uri) -> "PutOperations":
        """
        Constructs a collection of operations to upload the single file at
        `path` to `uri`.
        """

        if uri.uri.endswith("/"):
            uri /= path.name

        operations = PutOperations(path.parent, uri.parent)
        operations.add(path, uri)

        return operations

    @property
    def operations(self) -> List[PutOperation]:
        """
        Gets the operations ordered by local path.
        """

        def sort(a: PutOperation) -> Path:
            return a.path

        return sorted(self._operations, key=sort)
