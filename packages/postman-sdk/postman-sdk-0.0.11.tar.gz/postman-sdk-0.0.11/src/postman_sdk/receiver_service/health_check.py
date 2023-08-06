"""
Health check module
"""
import threading

# pylint: disable=W0622
from threading import Thread
from time import sleep
from http import HTTPStatus


from postman_sdk.receiver_service.client import call_reciever_api
from postman_sdk.receiver_service.config import (
    HEALTHCHECK_PATH,
    DEFAULT_HEALTH_PING_INTERVAL_SECONDS,
    EXPONENTIAL_BACKOFF_BASE,
)
from postman_sdk.util.constants import (
    HEALTH_CHECK_ERROR_COUNT_THRESHOLD,
)
from postman_sdk.util.logger import _LOG


class HealthCheck:
    """Health check module."""

    def __init__(self, postman_tracer):
        self.postman_tracer = postman_tracer
        self.lock = threading.Lock()
        self.default_health_ping_interval = DEFAULT_HEALTH_PING_INTERVAL_SECONDS

    def run(self):
        """Run health check in thread.

        Args:
            tracer(_type_): PostmanTracer
        """
        daemon = Thread(
            target=self.__health_poller,
            args=[],
            daemon=True,  # Main thread doesn't wait for this thread before being finished
            name="Postman SDK heath check poller",
        )
        daemon.start()
        return daemon

    def call_health_check_api(self):
        payload = {
            "sdk": {
                "collectionId": f"{self.postman_tracer.config.collection_id}",
                "enabled": self.postman_tracer.config.enable,
            }
        }

        return call_reciever_api(
            config=self.postman_tracer.config, path=HEALTHCHECK_PATH, payload=payload
        )

    def __health_poller(self, retry_count=0):
        if not self.default_health_ping_interval:
            return

        while True:
            if retry_count > 1:
                _LOG.debug(f"Retrying healthcheck retry no: {retry_count}")
            resp = self.call_health_check_api()

            if resp.status_code == HTTPStatus.OK.value:
                if resp.json().get("healthy"):
                    retry_count = 0
                    self.postman_tracer.unsuppress()

                sleep(self.default_health_ping_interval)

            elif resp.status_code == HTTPStatus.CONFLICT.value:
                if not self.postman_tracer.bootstrap_sdk():
                    # This turns off the health-check thread
                    return

                sleep(self.default_health_ping_interval)

            elif resp.status_code == HTTPStatus.NOT_FOUND.value:
                if "healthy" in resp.json() and not resp.json()["healthy"]:
                    if not self.postman_tracer.bootstrap_sdk():
                        # This turns off the health-check thread
                        return
                    sleep(self.default_health_ping_interval)
                else:
                    # Case when url itself is wrong
                    self.postman_tracer.suppress()
                    # This turns off the health-check thread
                    return

            else:
                self.postman_tracer.suppress()
                if retry_count > HEALTH_CHECK_ERROR_COUNT_THRESHOLD:
                    _LOG.warning("Shutting down Postman SDK")
                    self.postman_tracer.disable()
                    # This turns off the health-check thread
                    return

                retry_count += 1
                sleep(
                    (EXPONENTIAL_BACKOFF_BASE**retry_count)
                    * self.default_health_ping_interval
                )
