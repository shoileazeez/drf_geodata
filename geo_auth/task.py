import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler

from .database import download_database

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(download_database, "interval", hours=6, id="database_task", replace_existing=True)

    scheduler.start()
    logging.info("✅ APScheduler started successfully!")