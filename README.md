# adsb-with-kinesis


During the AWS EMEA Innovate livestream on February 29, 2024, I presented a 10 minute talk on analytics, with Kinesis, Data Firehose, and QuickSight.

![Architecture](architecture.png?raw=true "Architecture")


To build the demo, I needed a Raspberry Pi (I have a Raspberry Pi Zero 2 W), and a Software-Defined Radio (I use a Nooelec NESDR SMArt v5).

On the Raspberry Pi, install dump1090. FlightAware has a maintained version with installation instructions at https://www.flightaware.com/adsb/piaware/install (no need to install piaware). With the SDR connected to the Pi, reboot and you should hopefully see JSON data at `/run/dump1090-fa/aircraft.json`

Next, log in to AWS and set up a Kinesis Data Stream. Take the data stream name, and region, and input it into the adsb-to-kinesis.py file, which needs to be run on the Raspberry Pi. I keep it running with `nohup python3 -u /home/pi/adsb-to-kinesis.py >> /home/pi/ADSB-to-Kinesis.log 2>&1 &`

Set up an Amazon Data Firehose to accept data from a Kinesis data stream, and output it to an S3 bucket. Keep the buffer size small, I use 1MiB and 10 seconds. 

In the S3 console, look inside the bucket used for the Firehose destination, and make sure that your JSON files are arriving every 10 or so seconds. 

Once the data is in the bucket, head over to QuickSight, and create a new dataset with the S3 bucket. You'll need a manifest file, which looks like
```
{
    "fileLocations": [
        {
            "URIPrefixes": [
                "s3://bucket-name-here/"
            ]
        }
    ],
    "globalUploadSettings": {
        "format": "JSON"
    }
}
```

In QuickSight, create a Points on Map visualization, and drag and drop the `lat` and `lon` fields into the Geospatial field wells. You'll start seeing flight data.

The first three letters of the `flight` field contains the airline (ex. DLH = Lufthansa). Create a calculated field named `calculated-airline`, and enter `left(flight,3)`. Now drag the `calculated-airline` field into the Color field well, and the map data will update to show flights organized by colour. A tree map visualization with `calulated-airline` will display how many data points have been collected from each airline.
