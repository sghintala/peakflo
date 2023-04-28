import datetime
import calendar
from math import ceil
import csv

PEAK = "peak"
NONPEAK = "nonPeak"
DAILY = "daily"
WEEKLY = "weekly"

rate_card = {
    "Green": {

        "Red": {PEAK:4 , NONPEAK: 3},
        "Green": {PEAK: 2, NONPEAK: 1 },
    } ,
    "Red" : {

        "Red": {PEAK: 3, NONPEAK:  2  },
        "Green": {PEAK: 3  , NONPEAK:  2},
    }
}

max_fare= {
    "Green": {

        "Red": {"daily":15 , "weekly": 90},
        "Green": {"daily":8 , "weekly":55}
    } ,
    "Red" : {

        "Red": {"daily":1 , "weekly": 1},
        "Green": {"daily":15, "weekly": 90}
    }
}

peak_hours = {

    0: {"peak": [("080000", "100000"), ("163000", "190000")]  }, # Monday
    1: {"peak": [("080000", "100000"), ("163000", "190000")]  },
    2: {"peak": [("080000", "100000"), ("163000", "190000")]  },
    3: {"peak": [("080000", "100000"), ("163000", "190000")]  },
    4: {"peak": [("080000", "100000"), ("163000", "190000")]  },
    5: {"peak": [("100000", "140000"), ("180000", "230000")]  },
    6: {"peak": [("NA", "NA"), ("1800", "2300")]  } # Sunday
}

def find_day_from_date(time):
    date_obj = datetime.datetime.fromisoformat(time)
    return date_obj.weekday()

def calculate_fare(start_line, end_line, time):
    day = find_day_from_date(time)
    time = time.split("T")[1]
    time = time.replace(':', '')
    peak_hr = peak_hours[day][PEAK]

    is_in_peak_hr = False

    for hr in peak_hr:
        if hr[0] != "NA" and int(hr[0]) <= int(time) <= int(hr[1]):
            is_in_peak_hr = True

    return rate_card[start_line][end_line][PEAK if is_in_peak_hr else NONPEAK]


test_data = [
    ("Green", "Green", "2021-03-24T07:58:30"),
    ("Green", "Red", "2021-03-24T09:58:30"),
    ("Red", "Red", "2021-03-25T11:58:30"),
    ("Red", "Red", "2021-03-23T11:58:30"),
]

def week_of_month(dt):
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))

def cal_user_fare(test_data):

    fare_calculated = {}
    fare_calculated_weekly = {}

    for data in test_data:
        date = data[2].split("T")[0]
        startLine = data[0]
        endLine = data[1]
        fare = calculate_fare(startLine, endLine, data[2])
        t =fare_calculated.get((startLine, endLine, date), 0) + fare
        fare_calculated[(startLine, endLine, date)] = min(t, max_fare[startLine][endLine][DAILY])

        date_obj = datetime.datetime.fromisoformat(data[2])
        week = week_of_month(date_obj)
        t = fare_calculated_weekly.get((startLine, endLine, week),0) + fare
        fare_calculated_weekly[(startLine, endLine, week)] = min(t, max_fare[startLine][endLine][WEEKLY])
    res =0
    
    for key, val in fare_calculated_weekly.items():
        res += val


    return res



rows = []
with open('data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        rows.append(tuple(row))

print(cal_user_fare(rows))