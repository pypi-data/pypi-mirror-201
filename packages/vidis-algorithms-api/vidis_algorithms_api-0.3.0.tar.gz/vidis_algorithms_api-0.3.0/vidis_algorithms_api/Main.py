from celery import Celery
import numpy as np
from vidis_algorithms_api import Task
from vidis_algorithms_api.core import settings


class TestAlgorithm(Task):
    name = "test-algorithm-api"

    def task(self, hyperspecter: np.ndarray, **kwargs) -> np.ndarray:
        print("Processing")
        return np.zeros_like(hyperspecter)

celery = Celery(
    "algorithms",
    backend=settings.CELERY_BACKEND,
    broker=settings.CELERY_BROKER
)

@celery.task(name="TEST-API")
def your_algorithm(*args, **kwargs):
    task = TestAlgorithm()
    task.run(*args, **kwargs)

