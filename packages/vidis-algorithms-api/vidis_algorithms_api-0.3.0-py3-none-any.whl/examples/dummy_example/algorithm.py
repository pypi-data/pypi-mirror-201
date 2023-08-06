from celery import Celery
import numpy as np
from vidis_algorithms_api import Task
from vidis_algorithms_api.core import settings


class Algorithm(Task):
    name = "test"
    
    def task(self, hyperspecter: np.ndarray, **kwargs) -> np.ndarray:
        return np.zeros(hyperspecter.shape[1:])


celery = Celery(
    "algorithms",
    backend=settings.CELERY_BACKEND,
    broker=settings.CELERY_BROKER
)

@celery.task(name="TEST-API")
def your_algorithm(*args, **kwargs):
    task = Algorithm()
    task.run(*args, **kwargs)

