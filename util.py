import datetime


# Converts time from a string to a datetime object (format needs to be '08:00:00')
def time_conversion(string_time):
    (time_hour, time_min, time_sec) = string_time.split(':')
    return datetime.timedelta(hours=int(time_hour), minutes=int(time_min), seconds=int(time_sec))