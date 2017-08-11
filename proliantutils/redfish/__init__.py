import retrying
from sushy import connector
from sushy import exceptions

connector.Connector._op = retrying.retry(
    retry_on_exception=(
        lambda e: isinstance(e, exceptions.ConnectionError)),
    stop_max_attempt_number=5,
    wait_fixed=4 * 1000)(connector.Connector._op)
