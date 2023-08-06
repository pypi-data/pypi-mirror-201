import os
import traceback
from functools import wraps

from prefect import context

from src.external.grpc.prefect_routing_pb2 import FlowInfo


def get_flow_info() -> FlowInfo:
    """
    Returns the info for the running flow run.

    Returns
    -------
    FlowInfo
        The info for the flow run.
    """
    prefect_meta = context.get_run_context().flow_run  # type: ignore
    flow_run_id = prefect_meta.id
    node_name = os.getenv("NODE_NAME", "no-name")
    return FlowInfo(flow_id=str(flow_run_id), node_name=node_name)


def error_handler(func):
    @wraps(func)  # Keep flow function name
    async def wrap(*args, **kargs):
        try:
            result = await func(*args, **kargs)
        except Exception as e:
            from src.external.grpc import (
                grpc_client,
            )  # dynamic import to avoid circle import

            stacktrace = traceback.format_exc().splitlines()
            grpc_client.send_failed_result(stacktrace)
            raise e
        return result

    return wrap
