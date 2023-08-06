import os
import sys

from pawapi.exceptions import InvalidJSONError
from pawapi.exceptions import InvalidTokenError
from pawapi.exceptions import NotFoundError
from pawapi.exceptions import PermissionDeniedError
from pawapi.exceptions import RequestTimeoutError
from pawapi.exceptions import StatusError

if not __package__:
    pawcli_package_source = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, pawcli_package_source)

from pawcli.app import app
from pawcli.core.config import APP_NAME


def run() -> int:
    try:
        app(prog_name=APP_NAME)
    except (
        InvalidTokenError,
        NotFoundError,
        RequestTimeoutError,
        PermissionDeniedError,
        InvalidJSONError,
    ) as error:  # yapf: disable
        print(error)
    except StatusError as error:
        if error.description is None:
            print(f"Request failed with status {error.status_code}")
        else:
            print(error)
    else:
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(run())
