import json
import datetime
from api import dexcomAPI


# Pretty Print JSON
def pp_json(json_data):
    return json.dumps(json_data, indent=4, sort_keys=True)


# Returns hour and minute timestamp
def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M - ")


# Write your Dexcom Application implementation here
def main():
    print(get_timestamp() + "Starting Dexcom Application")
    print(pp_json(dexcomAPI("egvs")))


if __name__ == '__main__':
    main()