from typing import List, TypedDict


class StackOutput(TypedDict):
    OutputKey: str
    OutputValue: str
    Description: str | None


class Stack(TypedDict):
    Outputs: List[StackOutput]


class DescribeStacksResponse(TypedDict):
    Stacks: List[Stack]
