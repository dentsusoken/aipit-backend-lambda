import json
import logging
import typing

from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3ServiceResource

from constants import BUCKET_NAME, OBJECT_NAME


def put_object(
    s3_resource: S3ServiceResource,
    json_obj: typing.Any,
    bucket_name: str | None = None,
    object_name: str | None = None,
) -> bool:
    """Put an object to a S3 bucket

    :param json_obj: New S3 json object body
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    """

    if bucket_name is None:
        bucket_name = BUCKET_NAME

    if object_name is None:
        object_name = OBJECT_NAME

    # Put a object
    try:
        s3_obj = s3_resource.Object(bucket_name, object_name)
        s3_obj.put(Body=json.dumps(json_obj))

        return True
    except ClientError as e:
        logging.error(e)

        return False
