from celery import Celery
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# starts calery and loads tasks
# broker -> queues the tasks
# backend -> storage for task results
celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL, 
    include=["app.celery_tasks"]
    )
celery_app.autodiscover_tasks(["app"]) # define the task source

