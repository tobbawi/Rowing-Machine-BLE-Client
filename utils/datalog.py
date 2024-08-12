from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import datetime
import const
from stravalib.client import Client
import stravalib.exc
import pickle
import time

def generate_unique_filename(base_name='rowing_data_log'):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{const.BASE_LOG_DIR}/{base_name}_{timestamp}"
    return unique_filename

def get_client_id():
    try:
        f = open(const.MY_STRAVA_CLIENT_INFO, 'rb')
    except FileNotFoundError:
        print('No client info found, please run "python setup.py"')
    else:
        with f:
            client_info = pickle.load(f)
            return client_info['client_id']
        
def get_client_secret():
    try:
        f = open(const.MY_STRAVA_CLIENT_INFO, 'rb')
    except FileNotFoundError:
        print('NNo client info found, please run "python setup.py"')
    else:
        with f:
            client_info = pickle.load(f)
            return client_info['client_secret']

def get_access_token(client):
    access_token = None
    try:
        f = open(const.MY_STRAVA_ACCESS_TOKEN_FILE, 'rb')
    except FileNotFoundError:
        print('No access token file found, please run "python setup.py"')
    else:
        with f:
            access_token = pickle.load(f)

    if not access_token:
        print('You must authorize the app before uploading a file. Please run "python setup.py"')
        return
    
    if time.time() > access_token['expires_at']:
        print('Token has expired, will refresh')
        refresh_response = client.refresh_access_token(client_id=get_client_id(), client_secret=get_client_secret(), refresh_token=access_token['refresh_token'])
        access_token = refresh_response
        with open(const.MY_STRAVA_ACCESS_TOKEN_FILE, 'wb') as f:
            pickle.dump(refresh_response, f)
        print('Refreshed token saved to file')
        client.access_token = refresh_response['access_token']
        client.refresh_token = refresh_response['refresh_token']
        client.token_expires_at = refresh_response['expires_at']            
    else:
        print('Token still valid, expires at {}'
            .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))

    return access_token

def upload_strava(filename='rowing_data_log', title="Roeiathon", description="Roeien op de VirtuFit Ultimate Pro 2"):
    client = Client()

    access_token = get_access_token(client)

    print(f'Latest access token read from file: {access_token}')

    client.access_token = access_token['access_token']
    client.refresh_token = access_token['refresh_token']
    client.token_expires_at = access_token['expires_at']
    
    try:
        print(f'Opening file {filename}')
        tcx_file = open(filename, 'rb')
    except FileNotFoundError as e:
        print(f'Can not open {filename} {e}')
    else:
        with tcx_file: 
            print(f"Uploading {filename} to Strava as 'rowing' activity...")
            try:
                upload_response = client.upload_activity(
                    activity_file=tcx_file,
                    data_type='tcx',
                    name=title,
                    description=description,
                    activity_type='rowing'
                )

                activity = upload_response.wait(80, 5)
                if activity:
                    print("Activity uploaded to strava: {0}, {1} ({2})".format(activity.name,
                            activity.distance, filename))
            except stravalib.exc.ActivityUploadFailed as e:
                print('Activity upload failed', e)
            except stravalib.exc.ObjectNotFound as e:
                print('Object not found', e)
            except stravalib.exc.RateLimitExceeded as e:
                print('ratelimit', e)
            except stravalib.exc.TimeoutExceeded as e:
                print('Timeout', e)

def save_log(data_log, filename='rowing_data_log'):
    if not data_log:
        print("Data log is empty. No TXT file will be created.")
        return
    
    with open(filename, 'w') as f:
        for entry in data_log:
            f.write(f"{entry['timestamp']}: {entry['data']}\n")
    print(f"Data log saved to {filename}")

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
        #calories = SubElement(lap, 'Calories')
        #calories.text = str(rower_data.total_energy)
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

    with open(filename, 'w') as f:
        f.write(pretty_str)
    print(f"Data log saved to {filename}")