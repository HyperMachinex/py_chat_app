from celery_worker import celery_app
from datetime import datetime
import time

@celery_app.task
def generate_log():
    now = datetime.utcnow().isoformat()
    print(f"[{now}]  Worker is processing...")
    time.sleep(2)  
    print(f"[{now}]  Task completed.")
    return now

