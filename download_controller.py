from ERA5land_downloader import request_constructor, download, make_time, normalize_geometry
from functools import partial
import constants
import pandas as pd
import time
from dotenv import load_dotenv
import os
import logging
from concurrent.futures import ThreadPoolExecutor
# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename="era5land_downloader.log")
logger = logging.getLogger("controller")

load_dotenv()

era5land_downloader = partial(download, dataset_name = constants.dataset_name)
rs_request = partial(request_constructor, request_variables = constants.variables, data_format = "grib", download_format = "unarchived")
hour = constants.make_hour_list()

rs_record = pd.read_json(os.getenv("RS_RECORD_PATH"))
target_dir = os.getenv("TARGET_DIR")

logger.info(f"controller initialized")

def download_city(row):
    city = row["city"]
    year = row["year"]
    month = row["month"]
    day = row["day"]
    geometry = row["geometry"]["coordinates"][0]

    file_name = f"{city}_{year:04d}{month:02d}{day:02d}"
    target_path = os.path.join(target_dir, f"{file_name}.grib")
    time = make_time(year, month, day, hour)
    normal_geometry = normalize_geometry(geometry)
    era5land_request = rs_request(time = time, area = normal_geometry)
    try:
        era5land_downloader(selection_request = era5land_request, target_file = target_path)
        logger.info(f"Downloaded {file_name}")
    except Exception as e:
        if "400 Client Error" in str(e):
            logger.info("request this resource later")
            time.sleep(10)
            download_city(row)
        else:
            raise e

os.makedirs(target_dir, exist_ok=True)
with ThreadPoolExecutor(max_workers=9) as executor:
    executor.map(download_city, rs_record.to_dict(orient="records"))
#for row in rs_record.to_dict(orient="records"):
#    download_city(row)