from strawberry.types import ExecutionContext
from strawberry.types.graphql import OperationType


def is_mutation(execution_context: ExecutionContext) -> bool:
    try:
        return execution_context.operation_type == OperationType.MUTATION
    except RuntimeError as _:
        return False
