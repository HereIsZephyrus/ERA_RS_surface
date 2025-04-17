import cdsapi
import logging

logger = logging.getLogger("downloader")

def download(dataset_name, selection_request, target_file):
    client = cdsapi.Client()
    
    try:
        client.retrieve(dataset_name, selection_request, target_file)
    except Exception as e:
        logger.error(f"Error downloading {dataset_name}: {e}")
        raise e
    
def request_constructor(request_variables, data_format, download_format, time, area):
    """
    This function constructs a request for the ERA5-Land dataset.
    request_variables: list of variables to download
    data_format: format of the data to download, include "netcdf" or "grib"
    download_format: format of the data to download, include "unarchived" or "archived"
    time: dictionary with year, month, day, hour. In which day and hour can be a list of values.
    area: geometry bounding box to download, include [lat_min, lon_min, lat_max, lon_max]
    """
    year = time["year"]
    month = time["month"]
    day = time["day"]
    hour = time["hour"]

    if data_format not in ["netcdf", "grib"]:
        raise ValueError("Invalid data format")
    if download_format not in ["unarchived", "archived"]:
        raise ValueError("Invalid download format")
    
    request = {
        "variable": request_variables,
        "year": year,
        "month": month,
        "day": day,
        "time": hour,
        "data_format": data_format,
        "download_format": download_format,
        "area": area
    }
    
    return request

def make_time(year, month, day, hour):
    """
    This function constructs a time dictionary for the ERA5-Land dataset.
    """
    if not isinstance(hour, list):
        hour = [hour]
    if not isinstance(day, list):
        day = [day]
        
    return {"year": year, "month": month, "day": day, "hour": hour}

def normalize_geometry(outbound_geometry):
    """
    This function normalizes the geometry for the ERA5-Land dataset.
    """
    down_left = outbound_geometry[0]
    up_right = outbound_geometry[2]

    min_lon, min_lat = down_left
    max_lon, max_lat = up_right

    if min_lat < -90 or max_lat > 90 or min_lon < -180 or max_lon > 180:
        raise ValueError("Invalid geometry")

    return [max_lat, min_lon, min_lat, max_lon]

