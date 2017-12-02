import csv
import json
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

csv_file_path = 'twitter-airline-sentiment/Tweets.csv'
json_file_path = 'data/Tweets.json'

def dateConvert(input, timeZone):
    input_list = input.split()
    date_list = input_list[0].split('-')
    month_str = date_list[1]
    date_str = date_list[2]

    """ all offset from 2015-01-01 """
    """ calcualte day offset """
    day_off = 0
    if month_str == "02":
        day_off += 31
    elif month_str == "03":
        day_off += 31 + 28
    elif month_str == "04":
        day_off += 31 + 28 + 31
    elif month_str == "05":
        day_off += 31 + 28 + 31 + 30
    elif month_str == "06":
        day_off += 31 + 28 + 31 + 30 + 31
    elif month_str == "07":
        day_off += 31 + 28 + 31 + 30 + 31 + 30
    elif month_str == "08":
        day_off += 31 + 28 + 31 + 30 + 31 + 30 + 31
    elif month_str == "09":
        day_off += 31 + 28 + 31 + 30 + 31 + 30 + 31
    elif month_str == "10":
        day_off += 31 + 28 + 31 + 30 + 31 + 30 + 31 + 30
    elif month_str == "11":
        day_off += 31 + 28 + 31 + 30 + 31 + 30 + 31 + 30 + 31
    elif month_str == "12":
        day_off += 31 + 28 + 31 + 30 + 31 + 30 + 31 + 30 + 31 + 30

    day_off += int(date_str)

    """ calculate second offset """
    hour_list = input_list[1].split(':')
    second_off = int(hour_list[0]) * 3600 + int(hour_list[1]) * 60 + int(hour_list[2])

    total_second = day_off * 86400 + second_off

    """ factor time zone difference, final output based on PST """
    if timeZone == "Hawaii":
        total_second -= 2 * 60 * 60
    elif timeZone == "Alaska":
        total_second -= 1 * 60 * 60
    elif timeZone == "Mountain Time (US & Canada)":
        total_second += 1 * 60 * 60
    elif timeZone == "Central Time (US & Canada)":
        total_second += 2 * 60 * 60
    elif timeZone == "Eastern Time (US & Canada)":
        total_second += 3 * 60 * 60
    elif timeZone == "Atlantic Time (Canada)":
        total_second += 4 * 60 * 60

    return total_second

def geoLocation(input, geolocator):
    try:
        location = geolocator.geocode(input)
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message" % (input))
        return [0,0]
    if not location:
        return [0,0]
    else:
        return [location.latitude, location.longitude]

def json_dump(data):
    with open(json_file_path, 'w') as outfile:
        outfile.write('[\n')
        for entry in data:
            json.dump(entry, outfile)
            outfile.write(',\n')
        outfile.write(']')

def main():
    data = []
    count = 1
    geolocator = Nominatim()
    with open(json_file_path, 'w', 1) as outfile:
        outfile.write('[\n')
        with open(csv_file_path, "r", encoding="utf-8") as f:
            next(f)
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                # print(count, len(line), line)
                print("line ", count)
                count += 1
                cord = line[11]
                loc = line[13]
                if cord != '' or loc != '':  # check if contain location information
                    date = None
                    coordinate = []
                    airline = ""
                    sentiment = ""
                    confidence = None

                    """ load coordinate """
                    if cord != '':
                        cord = cord.replace('[','').replace(']','')
                        cord_split = cord.split(',')
                        coordinate.append(float(cord_split[0]))
                        coordinate.append(float(cord_split[1]))
                    else:
                        coordinate = geoLocation(loc, geolocator)
                        print("process sleep ")
                        time.sleep(0.5)

                    """ load date """
                    date = dateConvert(line[12], line[14])

                    """ load arline """
                    airline = line[5]

                    """ load sentiment """
                    sentiment = line[1]

                    """ load confidence """
                    confidence = float(line[2])

                    """ push into the data """
                    entry = {
                            "date" : date, "coordinate" : coordinate, "airline" : airline, "sentiment" : sentiment, "confidence" : confidence
                        }
                    data.append(entry)

                    """ write to json file """
                    json.dump(entry, outfile)
                    outfile.write(',\n')



if __name__ == "__main__":
    main()