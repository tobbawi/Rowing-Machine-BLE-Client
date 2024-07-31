from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import datetime

def generate_unique_filename(base_name='rowing_data_log'):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{base_name}_{timestamp}"
    return unique_filename

def save_log(data_log, filename='rowing_data_log'):
    if not data_log:
        print("Data log is empty. No TXT file will be created.")
        return
    
    file_txt = f"{filename}.txt"
    with open(file_txt, 'w') as f:
        for entry in data_log:
            f.write(f"{entry['timestamp']}: {entry['data']}\n")
    print(f"Data log saved to {file_txt}")

def save_log_to_tcx(data_log, filename='rowing_data_log'):
    if not data_log:
        print("Data log is empty. No TCX file will be created.")
        return
    
    root = Element('TrainingCenterDatabase', xmlns='http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
    activities = SubElement(root, 'Activities')
    activity = SubElement(activities, 'Activity', Sport='Rowing')
    id_element = SubElement(activity, 'Id')
    id_element.text = data_log[0]['timestamp'].isoformat()

    for entry in data_log:
        rower_data = entry['data']

        lap = SubElement(activity, 'Lap', StartTime=entry['timestamp'].isoformat())
        total_time_seconds = SubElement(lap, 'TotalTimeSeconds')
        total_time_seconds.text = str(rower_data.elapsed_time)
        distance_meters = SubElement(lap, 'DistanceMeters')
        distance_meters.text = str(rower_data.total_distance)
        maximum_speed = SubElement(lap, 'MaximumSpeed')
        maximum_speed.text = str(rower_data.instantaneous_pace) 
        calories = SubElement(lap, 'Calories')
        calories.text = str(rower_data.total_energy)
        intensity = SubElement(lap, 'Intensity')
        intensity.text = 'Active'
        trigger_method = SubElement(lap, 'TriggerMethod')
        trigger_method.text = 'Manual'
        track = SubElement(lap, 'Track')

        trackpoint = SubElement(track, 'Trackpoint')
        time = SubElement(trackpoint, 'Time')
        time.text = entry['timestamp'].isoformat()
        distance = SubElement(trackpoint, 'DistanceMeters')
        distance.text = str(rower_data.total_distance)
        heart_rate_bpm = SubElement(trackpoint, 'HeartRateBpm')
        value = SubElement(heart_rate_bpm, 'Value')
        value.text = str(rower_data.heart_rate)
        cadence = SubElement(trackpoint, 'Cadence')
        cadence.text = str(rower_data.stroke_rate)
        extensions = SubElement(trackpoint, 'Extensions')
        tpx = SubElement(extensions, 'TPX', xmlns='http://www.garmin.com/xmlschemas/ActivityExtension/v2')
        watts = SubElement(tpx, 'Watts')
        watts.text = str(rower_data.instantaneous_power)

    tree_str = tostring(root, 'utf-8')
    parsed_str = parseString(tree_str)
    pretty_str = parsed_str.toprettyxml(indent="  ")

    file_tcx = f"{filename}.tcx"
    with open(file_tcx, 'w') as f:
        f.write(pretty_str)
    print(f"Data log saved to {file_tcx}")