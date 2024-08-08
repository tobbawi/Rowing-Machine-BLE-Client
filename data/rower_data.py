from collections import namedtuple

RowerData = namedtuple(
    "RowerData", [
        "stroke_rate",
        "stroke_count",
        "average_stroke_rate",
        "total_distance", # m
        "instantaneous_pace",
        "average_pace",
        "instantaneous_power", # W
        "average_power", # W
        "resistance_level", # unitless
        "total_energy", # kcal
        "energy_per_hour", # kcal/h
        "energy_per_minute", # kcal/min
        "heart_rate", # bpm
        "metabolic_equivalent", # unitless; metas
        "elapsed_time", # s
        "remaining_time" # s
    ]
)

def parse_rower_data(barray) -> RowerData:
    flag_more_data = bool(barray[0] & 0b00000001)
    flag_average_stroke_rate_present= bool(barray[0] & 0b00000010)
    flag_total_distance_present= bool(barray[0] & 0b00000100)
    flag_instantaneous_pace_present= bool(barray[0] & 0b00001000)
    flag_average_pace_present= bool(barray[0] & 0b00010000)
    flag_instantaneous_power_present= bool(barray[0] & 0b00100000)
    flag_average_power_present= bool(barray[0] & 0b01000000)
    flag_resistance_level_present= bool(barray[0] & 0b10000000)
    flag_expended_energy_present= bool(barray[1] & 0b00000001)
    flag_heart_rate_present= bool(barray[1] & 0b00000010)
    flag_metabolic_equivalent_present= bool(barray[1] & 0b00000100)
    flag_elapsed_time_present= bool(barray[1] & 0b00001000)
    flag_remaining_time_present= bool(barray[1] & 0b00010000)

    stroke_rate = None 
    stroke_count = None
    average_stroke_rate = None
    total_distance = None
    instantaneous_pace = None 
    average_pace = None 
    instantaneous_power = None 
    average_power = None 
    resistance_level = None
    total_energy = None 
    energy_per_hour = None 
    energy_per_minute = None
    heart_rate = None 
    metabolic_equivalent = None
    elapsed_time = None 
    remaining_time = None 

    i = 2  # start after the flags
    if flag_more_data == 0:
        stroke_rate = int.from_bytes(barray[i : i + 1], "little", signed=False)
        i += 1
        stroke_count = int.from_bytes(barray[i : i + 2], "little", signed=False)
        i += 2
    if flag_average_stroke_rate_present:
        average_stroke_rate = int.from_bytes(barray[i : i + 1], "little", signed=False)
        i += 1
    if flag_total_distance_present:
        total_distance = int.from_bytes(barray[i : i + 3], "little", signed=False)
        i += 3
    if flag_instantaneous_pace_present:
        instantaneous_pace = int.from_bytes(barray[i : i + 2], "little", signed=False)
        i += 2
    if flag_average_pace_present:
        average_pace = int.from_bytes(barray[i : i + 2], "little", signed=False)
        i += 2
    if flag_instantaneous_power_present:
        instantaneous_power = int.from_bytes(barray[i : i + 2], "little", signed=True)
        i += 2
    if flag_average_power_present:
        average_power = int.from_bytes(barray[i : i + 2], "little", signed=True)
        i += 2
    if flag_resistance_level_present:
        resistance_level = int.from_bytes(barray[i : i + 2], "little", signed=True)
        i += 2
    if flag_expended_energy_present:
        total_energy = int.from_bytes(barray[i : i + 2], "little", signed=False)
        energy_per_hour = int.from_bytes(barray[i + 2 : i + 4], "little", signed=False)
        energy_per_minute = int.from_bytes(barray[i + 4 : i + 5], "little", signed=False)
        i += 5
    if flag_heart_rate_present:
        heart_rate = int.from_bytes(barray[i : i + 1], "little", signed=False)
        i += 1
    if flag_metabolic_equivalent_present:
        metabolic_equivalent = int.from_bytes(barray[i : i + 1], "little", signed=False) / 10
        i += 1
    if flag_elapsed_time_present:
        elapsed_time = int.from_bytes(barray[i : i + 2], "little", signed=False)
        i += 2
    if flag_remaining_time_present:
        remaining_time = int.from_bytes(barray[i : i + 2], "little", signed=False)
        i += 2

    return RowerData(
        stroke_rate, 
        stroke_count, 
        average_stroke_rate, 
        total_distance, 
        instantaneous_pace, 
        average_pace, 
        instantaneous_power, 
        average_power, 
        resistance_level, 
        total_energy, 
        energy_per_hour, 
        energy_per_minute, 
        heart_rate, 
        metabolic_equivalent, 
        elapsed_time, 
        remaining_time, 
    )