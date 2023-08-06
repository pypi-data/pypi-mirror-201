import typing as T
import json
from fastapi.encoders import jsonable_encoder
from graphql import FormattedExecutionResult
from strawberry.extensions import SchemaExtension
from strawberry.types import ExecutionContext
from app.dbs import db
from app.api.context import Context
from app import logs
from quilt import utils

logger = logs.create_logger(__name__)


def clean_result_obj(
    execution_context: ExecutionContext,
) -> dict[str, T.Any] | FormattedExecutionResult:
    if not execution_context.result:
        return {}
    try:
        res = execution_context.result.formatted
        if type(res) is not dict:
            res = {"res": str(res)}  # type: ignore
        return res
    except AttributeError as e:
        logger.error(f"{e=}, {execution_context.result=}")
    return {"res": str(execution_context.result)}


async def save_call(execution_context: ExecutionContext) -> None:
    context: Context = execution_context.context
    calls_config = context.config.calls
    if calls_config.ignore_all:
        logger.debug("ignoring call")
        return None
    if calls_config.ignore_variables:
        logger.debug("ignoring variables")
        variables = None
    else:
        variables = json.dumps(jsonable_encoder(execution_context.variables))
    request = context.request
    response = context.response
    insert = db.CallInsert(
        result=json.dumps(clean_result_obj(execution_context)),
        request_method=request.method,
        request_headers=json.dumps(jsonable_encoder(dict(request.headers))),
        request_url=str(request.url),
        request_id=execution_context.context.request_id,
        response_status_code=response.status_code,
        operation_name=execution_context.operation_name,
        query_str=execution_context.query,
        variables=variables,
        sentry_transaction_id=None,  # FUTURE add
    )

    if auth_id := context.auth.auth_id:
        insert.user = db.UserResolver().filter_by(auth_id=auth_id)
        if admin_auth_id := context.auth.admin_auth_id:
            insert.admin = db.UserResolver().filter_by(auth_id=admin_auth_id)

    call = await db.CallResolver().insert_one(insert=insert)
    logger.debug(f"INSERTED CALL, {call.id=}!")


class CallsExtension(SchemaExtension):
    async def on_request_end(self) -> None:
        if not utils.is_mutation(self.execution_context):
            return None
        self.execution_context.context.background_tasks.add_task(
            save_call, execution_context=self.execution_context
        )
