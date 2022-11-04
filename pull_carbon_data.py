#!/usr/bin/env python3

import sys
import os
import datetime
import requests
import time

BASE_URL = 'http://api.carbonintensity.org.uk'


# Earliest date for which we can access data.  This value was
# discovered experimentally.
#
# Trying to access data for a date that is earlier than earliest_date
# returns a valid JSON document with no data and a successful HTTP
# response code.  Note that, according to the Intensity schema, we an
# explicit 'data' property is not technically required.  Also note
# that this date occurs during BST (British Summer Time).
#
# $ curl -X GET https://api.carbonintensity.org.uk/intensity/date/2017-09-12 -H 'Accept: application/json'
# {
#   "data":[{ 
#     "from": "2017-09-11T23:00Z",
#     "to": "2017-09-11T23:30Z",
#     "intensity": {
#       "forecast": 134,
#       "actual": 140,
#       "index": "low"
#     }
#   },
# 
#   ...
#   
#   { 
#     "from": "2017-09-12T22:30Z",
#     "to": "2017-09-12T23:00Z",
#     "intensity": {
#       "forecast": 212,
#       "actual": 205,
#       "index": "moderate"
#     }
#   }]
# }
#
# $ curl -X GET https://api.carbonintensity.org.uk/intensity/date/2017-09-11 -H 'Accept: application/json' -w "\n%{response_code}\n"
# {
#   "data":[]
# }
# 200

EARLIEST_DATE = datetime.date.fromisoformat('2017-09-12')


def pull_one_day(d):
    
    headers = {
        'Accept': 'application/json'
    }

    r = requests.get('{base_url}/intensity/date/{date}'.format(base_url=BASE_URL, date=d),
                     params={}, headers=headers)
    return r.json()


def pull_all_days():

    # List of intensity data, where each element is to be a dict.  The
    # sortedness invariant is the 'from' key in each dict.  Sortedness
    # is maintained as the list is populated.
    intensity_data = []

    d = EARLIEST_DATE
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)

    while (d <= today):

        print('Pulling data for {date}'.format(date=d))
        j = pull_one_day(d)

        # Sort the intensity data because the API doesn't specify that the
        # 'data' property (a list object) will be sorted according to time.
        #
        # HACK: Python versions < 3.11 do not support the 'Z' suffix so we
        # must remove it (drop the last character).
        j['data'].sort(key=lambda intensity: datetime.datetime.fromisoformat(intensity['from'][:-1]))

        # Maintain the sortedness of intensity_data
        intensity_data.extend(j['data'])

        # Simple throttling so as not to overload the API; adjust this
        # factor as needed or use something like the throttle package.
        time.sleep(0.1)

        d += one_day

    return intensity_data


def main():
    if (len(sys.argv) != 2):
        sys.stderr.write("Usage: pull_carbon_data.py output_filename\n")
        sys.exit(1)
    else:
        intensity_data = pull_all_days()
        fname = sys.argv[1]
        with open(sys.argv[1], "w") as outfile:
            for i in intensity_data:
                line = '{frm}\t{to}\t{forecast}\t{actual}'.format(frm=i['from'],
                                                                  to=i['to'],
                                                                  forecast=i['intensity']['forecast'],
                                                                  actual=i['intensity']['actual'])
                outfile.write(line)
                outfile.write(os.linesep)

if __name__ == '__main__':
    main()
