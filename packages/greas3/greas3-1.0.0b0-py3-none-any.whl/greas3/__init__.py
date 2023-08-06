"""
## Introduction

**Greas3** is a Python package and command line application for uploading files
to Amazon Web Services S3 like a greased thing.

Rather rely on timestamps to detect changes, Greas3 uses SHA256 checksums to
avoid re-uploading identical files. Since [Git does not record file modification
timestamps](https://stackoverflow.com/questions/2179722/checking-out-old-files-with-original-create-modified-timestamps/2179825#2179825),
this makes Greas3 ideal for CI/CD pipelines that pull large files to upload to S3.

## Installation

Greas3 requires Python 3.9 or later and can be installed from
[PyPI](https://pypi.org/project/greas3/).

```shell
pip install greas3
```

## Command line usage

To upload a local file or directory to S3, run:

```text
greas3 LOCAL-PATH S3-URI
```

For example:

```shell
$ greas3 ./clowns.jpg s3://circus/clowns.jpg

/home/cariad/   s3://circus/
clowns.jpg    = clowns.jpg
```

To keep the original filename in S3, provide only the key prefix to upload to:

```shell
$ greas3 ./clowns.jpg s3://circus/

/home/cariad/   s3://circus/
clowns.jpg    = clowns.jpg
```

Pass a directory instead of a file to recursively upload its contents:

```shell
$ greas3 ./party-time/ s3://circus/inbox/

/home/cariad/party-time/   s3://circus/inbox/
good-clowns/steve.jpg    = good-clowns/steve.jpg
evil-clowns/jacob.jpg    = evil-clowns/jacob.jpg
```

Pass `--dry-run` to view the enqueued uploads without performing them:

```shell
$ greas3 ./party-time/ s3://circus/inbox/

/home/cariad/party-time/   s3://circus/inbox/
good-clowns/steve.jpg    = good-clowns/steve.jpg
evil-clowns/jacob.jpg    = evil-clowns/jacob.jpg
group-hug.jpg            > group-hug.jpg
```

`=` indicates that a file hasn't changed and so won't be uploaded. `>` indicates
the file will be uploaded.

## Python usage

The `put()` function accepts a path to a local file or directory and a
destination [S3 URI](https://cariad.github.io/slash3/) to upload to.

The function returns a list of `PutOperation`, each of which describes the
source file, destination URI and flag to indicate if the files are the same;
in which case the upload will not be performed.

To gather the operations without performing them, pass the `dry_run=True` flag.

## Authorisation

Greas3 will authenticate into Amazon Web Services using the first set of
credentials that the SDK finds.

Generally, in order of precedence, credentials are found in:

1. (When using the Python package) A Boto3 session with custom credentials can
be passed to functions.
1. The `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN`
environment variables.
1. A `credentials` or `config` file created by the AWS CLI. The `AWS_PROFILE`
environment variable can prescribe any non-default profile.

Greas3 requires the following actions:

- `s3:GetObjectAttributes`
- `s3:PutObject`

## How does it work?

To check if a file should be uploaded, Greas3 calls the S3
[GetObjectAttributes](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObjectAttributes.html)
API to gather the existing object's file size and SHA256 checksum (both the
file's checksum and each individual uploaded chunk's checksum).

If the file doesn't exist in S3, or if the file size is different from the local
file, then the files are considered different.

If the file was previously uploaded to S3 in chunks, and if each chunk has a
SHA256 checksum, then each chunk's checksum is compared to the local file's
equivalent byte range. If the checksums don't match then the files are
considered different.

If the object was previously uploaded to S3 in a single chunk then its checksum
is compared to the local file. If the checksums don't match then the files are
considered different.

Note that S3 will record checksums only if directed to during upload; other
tools might not request this but Greas3 does. If the checksums aren't present
then Greas3 will have to perform the upload even if the files are identical;
however, subsequent use of Greas3 will use the checksums to perform only uploads
that are strictly necessary.

## Time comparisons

I created a directory containing 10 files with a total of 117 MB, then --
pitching the AWS CLI and Greas3 against each other -- I:

1. Synchronised that directory with an S3 bucket.
1. Synchronised that directory again without making any changes.
1. Synchronised that directory again after touching the local files'
modification timestamps.

| Upload                     | AWS CLI (seconds) | Greas3 | Greas3 vs AWS CLI      |
| -                          |                -: |     -: | -                      |
| Initial                    |               ~51 |    ~56 | ~5 seconds slower      |
| No changes                 |                ~1 |     ~2 | ~1 second slower       |
| Touched modification dates |               ~51 |     ~2 | **~49 seconds faster** |

The AWS CLI is marginally more performant during the initial upload and when
timestamps can be trusted.

However, in an environment where timestamps can't be trusted -- for example, in
CI/CD pipelines that pull files from Git repositories -- Greas3 is clearly the
most performant uploader.

## Support

Please submit all your questions, feature requests and bug reports at
[github.com/cariad/greas3/issues](https://github.com/cariad/greas3/issues).
Thank you!

## Licence

Greas3 is [open-source](https://github.com/cariad/greas3) and published under
the [MIT License](https://github.com/cariad/greas3/blob/main/LICENSE).

You don't have to give attribution in your project, but -- as a freelance
developer with rent to pay -- I appreciate it!

## The Author

Hello! 👋 I'm **Cariad Eccleston**, and I'm a freelance Amazon Web Services
architect, DevOps evangelist, CI/CD deployer and backend developer.

You can find me at [cariad.earth](https://cariad.earth),
[github/cariad](https://github.com/cariad),
[linkedin/cariad](https://linkedin.com/in/cariad) and on Mastodon at
[@cariad@tech.lgbt](https://tech.lgbt/@cariad).
"""

from importlib.resources import open_text

from greas3.operations import put
from greas3.put_operation import PutOperation

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "put",
    "PutOperation",
]
