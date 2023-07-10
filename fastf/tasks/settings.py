import os
from functools import lru_cache
from typing import Any

from kombu import Queue


# noqa
def route_task(
    name: str,
    args: Any,
    kwargs: Any,
    options: Any,
    task: Any = None,
    **kw: dict[str, Any]
) -> dict[str, str]:
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL",
        "amqp://guest:guest@localhost:5672//",
    )
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "rpc://")

    CELERY_TASK_QUEUES: tuple[Any, Any, Any] = (
        # default queue
        Queue("celery"),
        # custom queue
        Queue("universities"),
        Queue("university"),
    )

    CELERY_TASK_ROUTES = (route_task,)


class DevelopmentConfig(BaseConfig):
    pass


@lru_cache()
def get_settings() -> DevelopmentConfig:
    config_cls_dict = {
        "development": DevelopmentConfig,
    }
    config_name = os.environ.get("CELERY_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
