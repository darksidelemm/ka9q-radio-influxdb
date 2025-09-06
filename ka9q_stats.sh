#!/bin/bash
#
# ka9q-radio -> InfluxDB Collection Script
#
# Run with cron on whatever update rate you want
#

# The 'control channel' of the ka9q-radio server you want to poll
# For WSPRDaemon setups this is typically hf.local
export KA9Q_SERVER="hf.local"
# A valid SSRC of an active channel on the server.
export KA9Q_SSRC="7074000"


# InfluxDB Settings
export INFLUXDB_URL="http://localhost:8086"
export INFLUXDB_TOKEN=""
export INFLUXDB_ORG=""
export INFLUXDB_BUCKET=""
export INFLUXDB_MEASNAME="ka9q_stats"

# Use a local venv if it exists
VENV_DIR=venv
if [ -d "$VENV_DIR" ]; then
    echo "Entering venv."
    source $VENV_DIR/bin/activate
fi

python3 ka9q_stats.py
