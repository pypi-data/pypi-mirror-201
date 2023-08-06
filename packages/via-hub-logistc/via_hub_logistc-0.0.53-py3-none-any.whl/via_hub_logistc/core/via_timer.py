from datetime import datetime
from robot.api import Error

class Timer():
    ### calculate  date in two date###
    def interval(start, end):
        try:

            d1 = datetime.strptime(start, '%Y%m%d %H:%M:%S.%f')
            d2 = datetime.strptime(end, '%Y%m%d %H:%M:%S.%f')

            return d2 - d1

        except Exception as e:
            raise Error(e)

    ### return on a date in format string###
    def str_to_date(value, format):
        try:
            return datetime.strptime(value, format)
        except Exception as e:
            raise Error(e)
