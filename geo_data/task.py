from apscheduler.schedulers.background import BackgroundScheduler
from .database import download_database
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def start_scheduler():
    scheduler = BackgroundScheduler()

    # logging.info("⏳ Running initial database download...")
    # download_database()
    # Schedule the task to run every 6 hours
    scheduler.add_job(download_database, "interval", hours=6, id="database_task", replace_existing=True)
    
    scheduler.start()
    logging.info("✅ APScheduler started successfully!")