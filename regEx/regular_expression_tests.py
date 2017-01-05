import re

time = r"([0-2]\d:[0-5]\d:[0-5]\d)(AM|PM)"
date = r"([0-1]\d/[0-3]\d/\d{4})"
latitude = r"(\+|\-)?(\d{2}\.\d+)"

if re.search(time, "09:54:00PM"):
    print ("time OK")

if re.search(date, "09/24/1990"):
    print("date OK")

if re.search(latitude, "+54.9864"):
    print ("latitude OK")