import requests
import zipfile
import os
import io
import logging
import glob

# Configuration
TOKEN = "I2xXJcpHzSk2sBGdI9olludJXo0uf7qCPtA0VInChCfaUFcTcknNUss0SBOpTH5a"
DATABASES = {
    "DB11LITEBIN": "IP2LOCATION-LITE-DB11.BIN",  # Location database
    "PX12LITEBIN": "IP2PROXY-LITE-PX12.BIN"  # Proxy database
}
OUTPUT_DIRECTORY = "iplite_database"

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

