dataset_name = "reanalysis-era5-land"
variables = [
    "2m_dewpoint_temperature",
    "2m_temperature",
    "skin_temperature",
    "soil_temperature_level_1",
    "soil_temperature_level_2",
    "soil_temperature_level_3",
    "soil_temperature_level_4",
    "lake_shape_factor",
    "lake_total_layer_temperature",
    "evaporation_from_bare_soil",
    "total_evaporation",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "surface_pressure",
    "total_precipitation",
    "leaf_area_index_high_vegetation",
    "leaf_area_index_low_vegetation",
    "high_vegetation_cover",
    "type_of_high_vegetation",
    "type_of_low_vegetation"
]
hour_list = range(10,14)
time_zone = 8 # Beijing Time UTC+8
def make_hour_list():
    return [f"{hour-time_zone:02d}:00" for hour in hour_list]