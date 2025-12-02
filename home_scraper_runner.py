import time
import subprocess
import logging
from pathlib import Path

# Local residential scraper runner (run this on your home machine, NOT in cloud)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/home_scraper.log"),
        logging.StreamHandler(),
    ],
)


def run_scraper_once():
    """Run the Playwright/PRO scraper once."""
    logging.info("🚀 Starting home scraper run (instagram_scraper_pro.py)")

    # Make sure data/raw_images exists
    Path("data/raw_images").mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            ["python", "1_scraper/instagram_scraper_pro.py"],
            check=True,
        )
        logging.info("✅ Home scraper run completed")
    except subprocess.CalledProcessError as e:
        logging.error(f"Scraper failed: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🏠 StructCrew Home Scraper Runner")
    print("=" * 60)
    print("This should run on your residential machine (not in cloud).")
    print("It calls 1_scraper/instagram_scraper_pro.py once per run.")
    print("=" * 60)

    # For now: run once and exit.
    # You can hook this into Windows Task Scheduler / cron to run
    # multiple times per day (e.g. every 4–6 hours).
    run_scraper_once()


