#!/usr/bin/env python
#
# ka9q-radio to InfluxDB Collection
#
import sys
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import pprint
from ka9q_metadump import ka9q_metadump

# Collect Environment Variables
KA9Q_SERVER = os.environ.get("KA9Q_SERVER")
KA9Q_SSRC = os.environ.get("KA9Q_SSRC")
INFLUXDB_URL = os.environ.get("INFLUXDB_URL")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")
INFLUXDB_MEASNAME = os.environ.get("INFLUXDB_MEASNAME")


print(f"ka9q-radio server: \t{KA9Q_SERVER}")
print(f"SSRC: \t{KA9Q_SSRC}")

print(f"InfluxDB URL: \t{INFLUXDB_URL}")
print(f"InfluxDB Token: \t{INFLUXDB_TOKEN}")
print(f"InfluxDB Org: \t{INFLUXDB_ORG}")
print(f"InfluxDB Bucket: \t{INFLUXDB_BUCKET}")
print(f"InfluxDB Measurement Name: \t{INFLUXDB_MEASNAME}")


# Gather data from metadump
_metadump = ka9q_metadump(control=KA9Q_SERVER, ssrc=KA9Q_SSRC)

# Reformat into what we want to push into InfluxDB
fields = {}

try:
    fields['rf_gain'] = _metadump['rf_gain']
    fields['rf_atten'] = _metadump['rf_atten']
    fields['ad_level'] = _metadump['if_power']
    fields['ad_overrange'] = _metadump['ad_over']

except Exception as e:
    print(f"Error parsing fields: {str(e)}")


meas_point = {
    "measurement": INFLUXDB_MEASNAME,
    "tags": {"name": KA9Q_SERVER},
    "fields": fields
}

print(meas_point)

# Push into InfluxDB
write_client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=meas_point)

print("Done!")