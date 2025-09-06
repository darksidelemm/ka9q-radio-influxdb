# ka9q-radio-influxdb
I wrote this because I wanted to monitor the A/D level and front-end gain of a RX888mkII based [ka9q-radio](https://github.com/ka9q/ka9q-radio) server, to evaluate AGC operation.

It might not work everywhere, and might break if the metadump output format or field names change.

## Setup
```
python3 -m venv venv
pip install -r requirements.txt
```

Edit ka9q_stats.sh and update env vars with appropriate settings.

Setup crontab to run ka9q_stats.sh every minute, or whatever rate you want.


## InfluxDB Data Info
This script uses the ka9q-radio 'metadump' utility, which provides a snapshot of statistics from a server and particular SSRC channel.

We take a subset of the output from this, including:
* rf gain
* rf atten
* IF pwr (Which is the receiver A/D level in a RX888 system)
* A/D overrange count


Data is added in the following format:
```
{
    'measurement': 'ka9q_stats', 
    'tags': {'name': 'hf.local'}, 
    'fields': {
        'ad_level': -21.4,
        'rf_gain': 4.8,
        'rf_atten': 0,
        'overload_count': 1933801
        }
}
```