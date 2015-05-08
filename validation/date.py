__author__ = 'paulo.rodenas'

from datetime import datetime


class Date(object):

    BRAZILIAN_FORMAT = '%d/%m/%Y'

    @staticmethod
    def parse(date_str, date_format=BRAZILIAN_FORMAT):
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            return None

    @staticmethod
    def format(date, date_format=BRAZILIAN_FORMAT):
        try:
            return datetime.strftime(date, date_format)
        except ValueError:
            return None