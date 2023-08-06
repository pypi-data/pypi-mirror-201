'''
Contains the `TradeBar` class, an abstract representation
of an equity's price values constructed using historical
data.
'''

import datetime
from . import resolution

class TradeBar:
    def __init__(
            self,
            resolution: resolution.Resolution,
            open: float,
            high: float,
            low: float,
            close: float,
    ) -> None:
        self.resolution = resolution
        self.Open = open
        self.High = high
        self.Low = low
        self.Close = close
    def setDate(self, date: datetime.datetime) -> None:
        '''
        Sets the date property for this `TradeBar`
        instance as an integer that can be easily
        sorted in acsending or descending order
        through SQL queries.

        The date property is formatted from left to
        right in this order:\n
        - Year with century as a decimal number (ie. 1999, 2012)\n
        - Day of the year as a zero-padded decimal number (001, 002, ...,366)\n
        - Hour (24-hour clock) as a zero-padded decimal number (00, 001, ..., 23)\n
        - Minute as a zero-padded decimal number (00, 001, ..., 59)\n

        '''
        self.date = int(date.strftime("%Y%j%H%M"))
    
    def getResolution(self) -> resolution.Resolution:
        return self.resolution
    def getOpen(self) -> float:
        return self.Open
    def getHigh(self) -> float:
        return self.High
    def getLow(self) -> float:
        return self.Low
    def getClose(self) -> float:
        return self.Close