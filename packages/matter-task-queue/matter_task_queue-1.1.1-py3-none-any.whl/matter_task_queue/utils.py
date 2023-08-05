import warnings
import logging
import asyncio
from celery import current_app as current_celery_app
from celery.signals import worker_process_init, worker_process_shutdown
from .config import Config
from .celery_config import build_celery_config, CELERY_BEAT_CONFIG

warnings.filterwarnings("ignore", "SelectableGroups dict interface")


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


def run_task(task, *args, **kwargs):
    """
    Submits a task to the task-queue from a sync function.
    In a DEBUG environment, the task will be called from a single thread.
    Otherwise, it will be submitted to the broker's queue and executed in a separate microservice.
    @param task: The task to run
    @param args: Additional task args arguments
    @param kwargs: Additional task kwargs arguments
    """

    if Config.DEBUG:
        task.apply(args=args, kwargs=kwargs)
    else:
        task.apply_async(args=args, kwargs=kwargs)


async def run_task_async(task: object, *args: object, **kwargs: object):
    """
    Submits a task to the task-queue from an async function.
    @param task: The task to run
    @param args: Additional task args arguments
    @param kwargs: Additional task kwargs arguments
    """

    partial_delay = lambda: run_task(task, *args, **kwargs)
    await asyncio.get_running_loop().run_in_executor(None, partial_delay)


def async_to_sync(func, *args, **kwargs):
    """
    Runs an async function from a sync function, using the Celery global event loop.
    A global event loop is vital for async code execution from Celery.
    The reason is that the repeated calls to get_event_loop() across different threads, cause the creation of
    new event_loops (as opposed to one single global loop). This behavior would result in colliding
    event-loops and execution errors. In asyncio, each thread has its own unique eventloop, and this function sets
    the global one as the thread's local event-loop.
    @param func: The function to execute.
    @param args: Additional function args arguments
    @param kwargs: Additional function kwargs arguments
    @return: The function's return value
    """

    try:
        resp = loop.run_until_complete(func(*args, **kwargs))
    finally:
        asyncio.set_event_loop(None)
    return resp


def create_celery(
    task_module_paths: [str],
    celery_beat_schedule: dict = None,
    create_dead_letter_queue=True,
):
    celery_app = current_celery_app
    celery_app.conf.update(build_celery_config(create_dead_letter_queue))
    celery_app.conf.update(CELERY_BEAT_CONFIG)
    celery_app.conf.update(beat_schedule=celery_beat_schedule)
    celery_app.autodiscover_tasks(task_module_paths)

    return celery_app


@worker_process_init.connect()
def worker_process_init(**kwargs):
    logging.info("Worker Process Initialization started...")
    # Optional Process Init Code
    logging.info("Done Worker Process Initialization.")


@worker_process_shutdown.connect()
def worker_process_shutdown(**kwargs):
    logging.info(f"Worker process [{kwargs['pid']}] shutdown... -> Exit Code: [{kwargs['exitcode']}]")
    logging.info("Done worker process shutdown.")
