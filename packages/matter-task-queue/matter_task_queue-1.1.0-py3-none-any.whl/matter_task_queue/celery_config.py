import logging
import re
import boto3

from logging.handlers import RotatingFileHandler
from kombu import Queue

from celery.signals import after_setup_logger

from .config import Config

CELERY_DEFAULT_QUEUE = "high_priority_queue"
CELERY_LOW_PRIORITY_QUEUE = "low_priority_queue"
CELERY_DEAD_LETTER_QUEUE = "dead_letter_queue"


@after_setup_logger.connect
def setup_task_logger(logger, *args, **kwargs):
    setup_celery_logger(logger)


def get_sqs_attributes():
    """configure SQS specific attributes."""
    if Config.IS_ENV_LOCAL_OR_TEST:
        sqs = boto3.client("sqs", region_name=Config.AWS_REGION, endpoint_url=Config.AWS_ENDPOINT_URL)
    else:
        sqs = boto3.client("sqs", region_name=Config.AWS_REGION)

    response = sqs.list_queues(QueueNamePrefix=CELERY_DEAD_LETTER_QUEUE)
    if len(response.get("QueueUrls", [])) == 0:
        response = sqs.create_queue(
            QueueName=CELERY_DEAD_LETTER_QUEUE,
            Attributes={
                "DelaySeconds": "60",
                "MessageRetentionPeriod": "86400",  # 24h Retention
            },
        )
        queue_url = response.get("QueueUrl")
    else:
        queue_url = response.get("QueueUrls", []).pop()
    match = re.match(r".*/(\d+)/(.+)/?$", queue_url)
    account_number, queue_name = match.groups()
    queue_arn = f"arn:aws:sqs:{Config.AWS_REGION}:{account_number}:{queue_name}"

    return {"RedrivePolicy": f'{{"deadLetterTargetArn": "{queue_arn}", "maxReceiveCount": "10"}}'}


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": CELERY_DEFAULT_QUEUE}


def setup_celery_logger(logger):
    logger.setLevel(Config.CELERY_LOG_LEVEL)

    file = RotatingFileHandler(
        filename=Config.CELERY_LOG_FILE_PATH,
        encoding="utf-8",
        mode="a",
        maxBytes=1 * 1024 * 1024,
    )
    file.setLevel(Config.CELERY_LOG_LEVEL)
    logger.addHandler(file)

    for handler in logger.handlers:
        handler.setFormatter(TaskFormatter("[%(asctime)s -%(task_name)s- %(name)s - %(levelname)s] %(message)s"))
    return logger


class TaskFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from celery._state import get_current_task

            self.get_current_task = get_current_task
        except ImportError:
            self.get_current_task = lambda: None

    def format(self, record):
        task = self.get_current_task()
        if task and task.request:
            record.__dict__.update(task_id=task.request.id, task_name=task.name)
        else:
            record.__dict__.setdefault("task_name", "")
            record.__dict__.setdefault("task_id", "")
        return super().format(record)


def build_celery_config(create_dead_letter_queue: bool):
    sqs_attributes = get_sqs_attributes() if create_dead_letter_queue else {}
    return {
        "broker_url": Config.CELERY_BROKER_URL,
        "broker_transport_options": {
            "region": Config.AWS_REGION,
            "visibility_timeout": 1200,
            "queue_name_prefix": f"{Config.INSTANCE_NAME}-",
            "sqs-creation-attributes": sqs_attributes,
        },
        "task_queues": (
            Queue(CELERY_DEFAULT_QUEUE),
            Queue(CELERY_LOW_PRIORITY_QUEUE, queue_arguments={"x-queue-mode": "lazy"}),
        ),
        "task_routes": (route_task,),
        "worker_pool_restarts": True,
        "task_ignore_result": True,
        "worker_hijack_root_logger": False,
        "worker_enable_remote_control": False,
        "worker_send_task_events": False,
        "task_always_eager": Config.DEBUG and Config.IS_ENV_LOCAL_OR_TEST,
    }


CELERY_BEAT_CONFIG = {
    "traceback": True,
    "schedule": "/tmp/celerybeat-schedule.db",
}
