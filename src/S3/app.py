import json
import logging

from aws_lambda_typing.context import Context
from aws_lambda_typing.events import APIGatewayProxyEventV2

from modules.lambda_events import LambdaResponse
from create_s3_resource import create_s3_resource
from get_response import get_response
from put_object import put_object


def lambda_handler(event: APIGatewayProxyEventV2, context: Context) -> LambdaResponse:
    logging.info('start')
    s3_resource = create_s3_resource()

    if s3_resource is None:
        message = 'Can\'t create resource'
        logging.error(message)

        return get_response(500, message)

    logging.info('create resource finish')

    try:
        body = json.loads(event['body'])
        bucket_name = body['bucket_name'] if 'bucket_name' in body else None
        object_name = body['object_name'] if 'object_name' in body else None

    except Exception:
        message = 'The body must be in JSON format.'
        logging.error(message)

        return get_response(400, message)

    json_obj = {'message': 'This is sample'}
    result = put_object(
        s3_resource,
        json_obj,
        bucket_name=bucket_name,
        object_name=object_name
    )

    if result is False:
        message = 'Can\'t put a object'
        logging.error(message)

        return get_response(500, message)

    logging.info('put object finish')

    return get_response(200, 'S3 hello world')
