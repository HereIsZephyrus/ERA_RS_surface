from atmosphere_func import calc_average_wind_speed
import os
from dotenv import load_dotenv
import logging
import json
import csv

logger = logging.getLogger("filter")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename="era5land_filter.log")
load_dotenv()

nc_dir = os.getenv("NC_DIR")

def create_identifier(file):
    basename = file.split(".")[0]
    cityname, date = basename.split("_")
    year = date[:4]
    month = date[4:6]
    return {
        "city": cityname,
        "year": year,
        "month": month,
    }

def generate_LST_download_list(serach_dir):
    record_list = []
    count_dict = {}
    for file in os.listdir(serach_dir):
        if file.endswith(".nc"):
            nc_path = os.path.join(nc_dir, file)
            average, std = calc_average_wind_speed(nc_path)
            if (average < 1 and std < 0.5):
                record_list.append(create_identifier(file))
            cityname = file.split("_")[0]
            if cityname not in count_dict:
                count_dict[cityname] = 0
            count_dict[cityname] += 1
    logger.info(f"Found {len(record_list)} records")
    return record_list, count_dict

def aggregate_record_list(record_list):
    aggregate_dict = {}
    count_dict = {}
    for record in record_list:
        cityname = record["city"]
        year = record["year"]
        month = record["month"]
        if cityname not in aggregate_dict:
            aggregate_dict[cityname] = []
            count_dict[cityname] = 0
        aggregate_dict[cityname].append({
            'year': year,
            'month': month
        })
        count_dict[cityname] += 1
    return aggregate_dict, count_dict

if __name__ == "__main__":
    record_list, raw_count_dict = generate_LST_download_list(nc_dir)
    aggregate_list, filtered_count_dict = aggregate_record_list(record_list)
    # write to json file
    with open("LST_download_list.json", "w", encoding="utf-8", newline="") as f:
        json.dump(aggregate_list, f, ensure_ascii=False)
    with open("filtered_count.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["city", "count"])
        for city, count in filtered_count_dict.items():
            writer.writerow([city, count])
    with open("raw_count.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["city", "count"])
        for city, count in raw_count_dict.items():
            writer.writerow([city, count])