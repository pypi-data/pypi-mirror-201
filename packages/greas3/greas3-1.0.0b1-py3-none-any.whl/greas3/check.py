from base64 import b64decode
from os.path import getsize
from pathlib import Path

from boto3.session import Session
from checksome import SHA256, checksum_reader
from slash3 import S3Uri

from greas3.logging import logger


def are_same(local: Path, uri: S3Uri, session: Session) -> bool:
    """
    Checks if the file at `local` appears to be identical to the remote object
    at `uri`.
    """

    s3 = session.client("s3")

    try:
        response = s3.get_object_attributes(
            Bucket=uri.bucket,
            Key=uri.key.key,
            ObjectAttributes=["Checksum", "ObjectParts", "ObjectSize"],
        )

    except s3.exceptions.NoSuchKey:
        logger.debug("The remote doesn't exist")
        return False

    if response["ObjectSize"] != getsize(local):
        logger.debug("The objects are different lengths")
        return False

    with checksum_reader(local, SHA256) as cf:
        if "ObjectParts" in response:
            offset = 0

            while True:
                parts = response["ObjectParts"]

                try:
                    for part in parts["Parts"]:
                        length = part["Size"]
                        expect = b64decode(part["ChecksumSHA256"])

                        if not cf.has_checksum(
                            expect,
                            offset=offset,
                            length=length,
                        ):
                            return False

                        offset += length

                except KeyError as ex:
                    logger.error(
                        "No %s in get_object_attributes response (%s)",
                        str(ex),
                        repr(response),
                    )
                    raise

                total_parts = parts.get("TotalPartsCount", 0)
                next_marker = parts.get("NextPartNumberMarker", None)

                logger.debug(
                    "Checking pagination: "
                    "TotalPartsCount=%s, NextPartNumberMarker=%s",
                    total_parts,
                    next_marker,
                )

                if next_marker is None or next_marker == total_parts:
                    logger.debug("Finished paginating %s parts", total_parts)
                    return True

                logger.debug(
                    "Requesting next page: PartNumberMarker=%s",
                    next_marker,
                )

                response = s3.get_object_attributes(
                    Bucket=uri.bucket,
                    Key=uri.key.key,
                    ObjectAttributes=["ObjectParts"],
                    PartNumberMarker=next_marker,
                )

        expect = b64decode(response["Checksum"]["ChecksumSHA256"])
        return cf.has_checksum(expect)
