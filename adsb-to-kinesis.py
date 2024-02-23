import boto3
import json
import time
import os

kinesis_client      = boto3.client('kinesis', region_name='eu-central-1')
kinesis_stream_name = 'raspberry-pi-flightdata'
json_file_path      = '/run/dump1090-fa/aircraft.json'

def is_valid_aircraft_data(aircraft):
    alt_baro = aircraft.get('alt_baro', 0)
    alt_geom = aircraft.get('alt_geom', 0)
    gs = aircraft.get('gs', 0)
    ias = aircraft.get('ias', 0)
    tas = aircraft.get('tas', 0)

    return all([
        alt_baro < 50000,
        alt_geom < 50000,
        gs < 700,
        ias < 700,
        tas < 700
    ])

def stream_data():
    last_modified_time = None

    while True:
        current_modified_time = os.path.getmtime(json_file_path)

        if current_modified_time != last_modified_time:
            last_modified_time = current_modified_time

            with open(json_file_path, 'r') as file:
                data = json.load(file)
                for aircraft in data['aircraft']:
                    if 'lat' in aircraft and 'lon' in aircraft:
                        if is_valid_aircraft_data(aircraft):

                            response = kinesis_client.put_record(
                                StreamName   = kinesis_stream_name,
                                Data         = json.dumps(aircraft),
                                PartitionKey = 'partition_key'
                            )
                            print(f"Flight {aircraft.get('flight', 'Unknown ')} streamed to Kinesis.")

        # Wait for 4 seconds before checking the file again
        time.sleep(4)

if __name__ == "__main__":
    stream_data()
