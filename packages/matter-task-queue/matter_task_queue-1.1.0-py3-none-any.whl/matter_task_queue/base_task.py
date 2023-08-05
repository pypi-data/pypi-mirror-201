import logging

from celery import Task
from celery.worker.request import Request
from billiard.exceptions import WorkerLostError

from .config import Config


class BaseRequest(Request):
    def on_timeout(self, soft, timeout):
        super(BaseRequest, self).on_timeout(soft, timeout)
        if not soft:
            logging.error(f"A hard timeout was enforced for task {self.task.name}")

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        super().on_failure(exc_info, send_failed_event=send_failed_event, return_ok=return_ok)
        if isinstance(exc_info.exception, WorkerLostError):
            logging.error(f"Failure detected for task {self.task.name}: {str(exc_info.exception)}")
            if Config.SENTRY_DSN and not Config.IS_ENV_LOCAL_OR_TEST:
                from sentry_sdk import capture_exception

                capture_exception(exc_info.exception)


class BaseTask(Task):
    Request = BaseRequest

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error(f"Error Occurred: {str(exc)}")
        if Config.SENTRY_DSN and not Config.IS_ENV_LOCAL_OR_TEST:
            from sentry_sdk import capture_exception

            capture_exception(exc)
