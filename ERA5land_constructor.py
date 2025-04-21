import zipfile
import pandas as pd
import xarray as xr
from dotenv import load_dotenv
import os
import shutil
import logging

logger = logging.getLogger("constructor")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename="era5land_constructor.log")
load_dotenv()
target_dir = os.getenv("TARGET_DIR")
cache_dir = os.getenv("CACHE_DIR")
os.makedirs(cache_dir, exist_ok=True)
nc_dir = os.getenv("NC_DIR")
os.makedirs(nc_dir, exist_ok=True)
print(cache_dir, nc_dir)

def extract_grib(file):
    base_name = file.split(".")[0]
    extract_dir = os.path.join(cache_dir, base_name)
    orient_file = os.path.join(extract_dir, "data.grib")
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    else:
        return extract_dir, orient_file
    
    try:
        with zipfile.ZipFile(os.path.join(target_dir, file), "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    except Exception as e:
        logger.error(f"Error extracting {file}: {e}")
        return None, None
    return extract_dir, orient_file

def convert_grib_to_nc(zip_file):
    grib_dir, grib_file = extract_grib(zip_file)
    target_file = os.path.join(nc_dir, zip_file.split(".")[0] + ".nc")
    if os.path.exists(target_file):
        logger.info(f"File {target_file} already exists")
        return target_file
    try:
        os.system(f"grib_to_netcdf -o {target_file} {grib_file}")
    except Exception as e:
        logger.error(f"Error converting {grib_file} to {target_file}: {e}")
        return None
    
    try:
        shutil.rmtree(grib_dir)
    except Exception as e:
        logger.warning(f"Error removing {grib_dir}: {e}")

    logger.info(f"Converted {file} to nc format")
    return target_file
    
for file in os.listdir(target_dir):
    if not file.endswith(".zip"):
        continue
    nc_file = convert_grib_to_nc(file)