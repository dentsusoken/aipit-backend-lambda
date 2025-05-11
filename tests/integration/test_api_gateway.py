import os
from typing import Generator, cast

import boto3
import pytest
import requests


class TestApiGateway:
    @pytest.fixture()  # type: ignore[misc]
    def api_gateway_url(self) -> Generator[str, None, None]:
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError("Please set the AWS_SAM_STACK_NAME environment variable.")

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name}\n"
                f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [
            output for output in stack_outputs if output["OutputKey"] == "HelloWorldApi"
        ]

        if not api_outputs:
            raise KeyError(f"HelloWorldAPI not found in stack {stack_name}")

        yield cast(str, api_outputs[0]["OutputValue"])

    def test_api_gateway(self, api_gateway_url: str) -> None:
        response = requests.get(api_gateway_url)
        assert response.status_code == 200
        assert response.json() == {"message": "hello world"}
