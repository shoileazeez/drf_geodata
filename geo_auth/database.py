import glob
import io
import logging
import os
import zipfile

import requests
from django.conf import settings

TOKEN = settings.TOKEN

DATABASES = {
    "DB11LITEBIN": "IP2LOCATION-LITE-DB11.BIN",  # Location database
    "DBASNLITEBIN": "IP2LOCATION-LITE-ASN.BIN",  # ASN database
}
OUTPUT_DIRECTORY = "iplite_database"
# handle data download and extraction of zip file
def download_database():
    logging.info("🔄 Starting database download process...")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    # 🔥 Delete old database files
    for old_file in glob.glob(os.path.join(OUTPUT_DIRECTORY, "*")):
        os.remove(old_file)
        logging.info(f"🗑 Deleted old file: {old_file}")

    for db_code, db_filename in DATABASES.items():
        try:
            download_url = f"https://www.ip2location.com/download/?token={TOKEN}&file={db_code}"
            logging.info(f"⬇️ Downloading {db_filename}...")

            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            # Extract ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(OUTPUT_DIRECTORY)

            logging.info(f"✅ Successfully extracted {db_filename} to {OUTPUT_DIRECTORY}")

        except Exception as e:
            logging.error(f"❌ Error downloading {db_filename}: {e}")

