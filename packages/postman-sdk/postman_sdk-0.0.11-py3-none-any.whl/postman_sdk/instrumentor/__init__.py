"""
general instrumentor initialization module.
"""
from postman_sdk.instrumentor.postman_flask_instrumentation import FlaskInstrumentation
from postman_sdk.instrumentor.postman_requests_instrumentation import (
    RequestsInstrumentation,
)


def get_instrumentations(*args, **kwargs):
    """
    Initialize all possible instrumentation frameworks.
    """
    instrumentation = [FlaskInstrumentation, RequestsInstrumentation]

    return [
        instrumentation_instance(*args, **kwargs)
        for instrumentation_instance in instrumentation
    ]
