from types.cloudformation import DescribeStacksResponse

import pytest


@pytest.fixture()  # type: ignore[misc]
def mock_stack_response() -> DescribeStacksResponse:
    return {
        "Stacks": [
            {
                "Outputs": [
                    {
                        "OutputKey": "HelloWorldApi",
                        "OutputValue": "http://localhost:4566/restapis/abc/hello",
                        "Description": "Mock output",
                    }
                ]
            }
        ]
    }
