import requests
import zipfile
import os
import io
import logging
import glob

def download_database():
    logging.info("🔄 Starting database download process...")

    # Configuration
    token = "GUJM9VIfQ8tg6tsdS9ZKDVrmfbY9a6MgsUQ5PZKenfM3ijGMKjm9d8KfAFPKNqFU"
    database_code = "DB11LITEBIN"
    download_url = f"https://www.ip2location.com/download/?token={token}&file={database_code}"

    output_directory = "iplite_database"
    os.makedirs(output_directory, exist_ok=True)

    try:
        # 🔥 Delete old files before downloading the new one
        for old_file in glob.glob(os.path.join(output_directory, "*")):
            os.remove(old_file)
            logging.info(f"🗑 Deleted old file: {old_file}")

        logging.info("⬇️ Downloading new IPLite database...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        # Extract the ZIP file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(output_directory)

        logging.info(f"✅ Successfully extracted IPLite database to {output_directory}")

    except Exception as e:
        logging.error(f"❌ Error downloading database: {e}")

