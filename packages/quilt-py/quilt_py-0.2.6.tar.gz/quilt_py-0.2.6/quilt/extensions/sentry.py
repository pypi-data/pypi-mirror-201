import typing as T
import hashlib
from inspect import isawaitable
from typing import Optional

from sentry_sdk import configure_scope, start_span, set_user

from strawberry.extensions import SchemaExtension
from strawberry.extensions.tracing.utils import should_skip_tracing
from strawberry.types.execution import ExecutionContext
from strawberry.utils.cached_property import cached_property

from devtools import pformat

from quilt import logs, helpers

logger = logs.create_logger(__name__)

class SentryTracingExtension(SchemaExtension):
    def __init__(
        self,
        *,
        execution_context: Optional[ExecutionContext] = None,
    ):
        if execution_context:
            self.execution_context = execution_context

    @cached_property
    def _resource_name(self) -> str:
        assert self.execution_context.query

        query_hash = self.hash_query(self.execution_context.query)

        if self.execution_context.operation_name:
            return f"{self.execution_context.operation_name}:{query_hash}"

        return query_hash

    def hash_query(self, query: str) -> str:
        return hashlib.md5(query.encode("utf-8")).hexdigest()

    def on_request_start(self) -> None:
        self._operation_name = self.execution_context.operation_name or helpers.operation_name_from_query(self.execution_context.query)
        context = self.execution_context.context
        name = self._operation_name or 'Anonymous Query'
        if jwt_user := context.auth.jwt_user:
            d = {
                "operation": self._operation_name,
                "name": jwt_user.name,
                "auth_id": jwt_user.user_id,
                "request_id": str(context.request_id),
            }
            logger.info(pformat(d))
            set_user(
                {
                    "id": jwt_user.user_id,
                    "username": jwt_user.name,
                    "email": jwt_user.email,
                    "ip_address": context.req.ip_address,
                }
            )

        with configure_scope() as scope:
            if scope.span:
                self.gql_span = scope.span.start_child(
                    op="gql",
                    description=name,
                )
            else:
                self.gql_span = start_span(
                    op="gql",
                )
            if scope.transaction:
                scope.transaction.name = name
        operation_type = "query"

        assert self.execution_context.query

        if self.execution_context.query.strip().startswith("mutation"):
            operation_type = "mutation"
        if self.execution_context.query.strip().startswith("subscription"):
            operation_type = "subscription"

        self.gql_span.set_tag("graphql.operation_type", operation_type)
        self.gql_span.set_tag("graphql.resource_name", self._resource_name)
        self.gql_span.set_data("graphql.query", self.execution_context.query)

    def on_request_end(self) -> None:
        self.gql_span.finish()

    def on_validation_start(self) -> None:
        self.validation_span = self.gql_span.start_child(
            op="validation", description="Validation"
        )

    def on_validation_end(self) -> None:
        self.validation_span.finish()

    def on_parsing_start(self) -> None:
        self.parsing_span = self.gql_span.start_child(
            op="parsing", description="Parsing"
        )

    def on_parsing_end(self) -> None:
        self.parsing_span.finish()

    async def resolve(self, _next, root, info, *args, **kwargs) -> T.Any:  # type: ignore
        if should_skip_tracing(_next, info):
            result = _next(root, info, *args, **kwargs)

            if isawaitable(result):  # pragma: no cover
                result = await result

            return result

        field_path = f"{info.parent_type}.{info.field_name}"

        with self.gql_span.start_child(
            op="resolve", description=f"Resolving: {field_path}"
        ) as span:
            span.set_tag("graphql.field_name", info.field_name)
            span.set_tag("graphql.parent_type", info.parent_type.name)
            span.set_tag("graphql.field_path", field_path)
            span.set_tag("graphql.path", ".".join(map(str, info.path.as_list())))

            result = _next(root, info, *args, **kwargs)

            if isawaitable(result):
                result = await result

            return result


class SentryTracingExtensionSync(SentryTracingExtension):
    def resolve(self, _next, root, info, *args, **kwargs) -> T.Any:  # type: ignore
        if should_skip_tracing(_next, info):
            return _next(root, info, *args, **kwargs)

        field_path = f"{info.parent_type}.{info.field_name}"

        with self.gql_span.start_child(
            op="resolve", description=f"Resolving: {field_path}"
        ) as span:
            span.set_tag("graphql.field_name", info.field_name)
            span.set_tag("graphql.parent_type", info.parent_type.name)
            span.set_tag("graphql.field_path", field_path)
            span.set_tag("graphql.path", ".".join(map(str, info.path.as_list())))

            return _next(root, info, *args, **kwargs)
