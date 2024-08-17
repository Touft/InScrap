import schedule
import time
import config
import logger
from scrape_videos import run_scraping

log = logger.setup_logger('main')

def daily_scrape():
    log.info("Starting the daily scraping routine.")
    run_scraping(config.IG_USERNAME, config.IG_PASSWORD, config.OUTPUT_FOLDER, days=1)

schedule.every().day.at(config.DAILY_SCHEDULED_TIME).do(daily_scrape)

if __name__ == "__main__":
    log.info("Instagram bot started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
