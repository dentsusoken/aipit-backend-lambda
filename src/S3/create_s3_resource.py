import logging

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3ServiceResource

from constants import AWS_DEFAULT_REGION, AWS_ENDPOINT_URL


def create_s3_resource(
    endpoint: str = AWS_ENDPOINT_URL, region: str = AWS_DEFAULT_REGION
) -> S3ServiceResource | None:

    try:
        s3_resource = boto3.resource('s3', region_name=region, endpoint_url=endpoint)

    except ClientError as e:
        logging.error(e)

        return None

    return s3_resource
