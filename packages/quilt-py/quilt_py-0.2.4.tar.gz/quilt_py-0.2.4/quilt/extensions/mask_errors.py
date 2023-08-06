from graphql.error import GraphQLError
from strawberry.extensions import MaskErrors
import edge_orm
from quilt import DisplayException


def should_mask_error(error: GraphQLError) -> bool:
    # strawberry's validation errors
    if not error.original_error:
        return False
    return not isinstance(
        error.original_error,
        (
            DisplayException,
            PermissionError,
            edge_orm.ExecuteConstraintViolationException,
            edge_orm.PermissionsError,
        ),
    )


mask_errors = MaskErrors(
    error_message="Internal Server Error", should_mask_error=should_mask_error
)

__all__ = ["mask_errors"]
