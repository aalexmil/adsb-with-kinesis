# adsb-with-kinesis

If you have a Raspberry Pi with dump1090-fa installed, you'll see a JSON file at /run/dump1090-fa/aircraft.json

That file is frequently updated whenever there's a nearby aircraft.

The JSON can be sent to an AWS Kinesis Datastream, and then onwards to Data Firehose, S3, and then visualised in QuickSight.
