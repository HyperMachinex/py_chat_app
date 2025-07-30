# app/scheduler.py

import time
from app.celery_tasks import generate_log

if __name__ == "__main__":
    print("Scheduler has started...")
    while True:
        generate_log.delay()
        print("New task added to queue")
        time.sleep(5)

