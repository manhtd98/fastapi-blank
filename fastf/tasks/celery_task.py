from typing import Any, List

from api import universities
from celery import shared_task


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="universities:get_all_universities_task",
)
def get_all_universities_task(self: Any, countries: List[str]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for cnt in countries:
        data.update(universities.get_all_universities_for_country(cnt))
    return data


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="university:get_university_task",
)
def get_university_task(self: Any, country: str) -> list[Any]:
    university = universities.get_all_universities_for_country(country)
    return university
