'''
This module contains the base indicator class and all subclasses
that each represent a separate indicator.

Once instantiated, an indicator will be provided its own row in an SQL table
devoted solely to instances of that indicator type (ie. `RelativeStrengthIndex`,
`SimpleMovingAverage`). In this row, instance-oriented data such as the indicator's 
period, equity, and last calculated value will be stored.

Caching such information will provide both an extra measure of security and a means
of cyclically restoring past data in order to improve the efficiency of downstream
calculations. Long term data storage, as opposed to an in-memory cache, inherently 
produces a stable and reusable architecture perfectly suited for repetitive
yet discontinuous procedures executed, each time, using permutations of the same data.
    
In accordance with this nature, LocalTrader derives indicator values by combining small
slices of new data with minute arithmetic modifications of prior values that have been 
cached in the database. This negates the need for manipulating pre-existing data within 
the indicator period.

As an example, assuming LocalTrader is run once daily, calcualting the 14 period Relative
Strength Index of an equity requires only that the price of the equity on the current day
is inserted into the database. There is no need to iterate through every price from the
past 14 days to generate an accurate indicator value.

Additionally, the aforementioned process of updating indicator values reduces the load
placed on LocalTrader as well as the surface area for bugs or errors to permeate the 
program.
'''

import numpy as np
import sqlite3

class BaseIndicator:
    '''
    Base class containing general methods and properties used by all indicator
    subclasses.
    '''
    def __init__(self, period: int, equity: str, cursor: sqlite3.Cursor) -> None:
        self.period = period
        self.equity = equity
        self.cursor = cursor
        self.value = None
        self.last_value = self.get_cached_value()
        self.name = None
        self.updated = False
    def row_exists(self) -> bool:
        '''
        This method checks the SQlite database for a row in the 
        Indicator table that corresponds to this specific indicator
        instance.

        :rtype: `bool`
        '''
        # Column 'name' must be UNIQUE in 'indicators' table
        return self.cursor.execute(f"SELECT name FROM indicators WHERE name='{self.name}'").fetchone() is not None
        
    def get_cached_value(self) -> float:
        '''
        Retrieves the last indicator value from the 
        SQlite database for enhanced efficiency in calculating
        a current value.
        '''
        return float(self.cursor.execute(f"SELECT value FROM indicators WHERE name='{self.name}'").fetchone()[0])
    def set_cached_value(self) -> None:
        '''
        Sets the cached value in the database to the value
        specified in `self.period` if that value is not `None`.
        '''
        if self.value is not None:
            return self.cursor.execute(f"")
    def update_value(self, new_value=None) -> None:
        ''' 
        This is the parent implementation of the `update_value` method.
        It must be overwritten in all child classes as this method
        does not update an instance's `self.value` attribute.


        :param new_value: A new data point used to update the 
        indicator value.
        '''
        # Enforce type as float
        if new_value is not None:
            new_value = float(new_value)


class SimpleMovingAverage(BaseIndicator):
    def __init__(self, period: int, equity: str, cursor: sqlite3.Cursor) -> None:
        super(SimpleMovingAverage, self).__init__(period, equity, cursor)
    def update_value(self, new_value=None):
        '''
        This is a convenience method that allows for an updated
        indicator value to be calculated without first creating
        and committing a transaction in the database to store the
        new data that will be used to calculate the indicator's
        new value.

        :param new_value: A new data point used to update the 
        indicator value.
        '''
        super().update_value(new_value=new_value)



class RelativeStrengthIndex(BaseIndicator):
    def __init__(self, period: int, equity: str, cursor: sqlite3.Cursor) -> None:
        super(RelativeStrengthIndex, self).__init__(period, equity, cursor)
    
    def update_value(self, new_value=None) -> None:
        '''
        This is a convenience method that allows for an updated
        indicator value to be calculated without first creating
        and committing a transaction in the database to store the
        new data that will be used to calculate the indicator's
        new value.

        :param new_value: A new data point used to update the 
        indicator value.
        '''
        super().update_value(new_value=new_value)
    def calculate_rsi(self) -> None:
        '''
        Private method used to calculate an updated RSI value over the 
        period specified in `self.period`.
        '''
        super().get_cached_value()

    def compute_average_returns(self, open_data: list[float], close_data: list[float]) -> None:
        '''
        Calculates and sets the average gain and average loss over the past n periods
        using closing prices from parameter `close_data` and opening prices from parameter
        `open_data`.

        :param open_data: A sequence of floating point values representing an equity's
        opening prices over the past `self.period` trading days.

        :param close_data: A sequence of floating point values representing an equity's
        closing prices over the past `self.period` trading days.
        '''
        # Initialize list objects for isolated storage of gain and loss days needed to
        # calculate the RSI over the specified period.
        gains = list()
        losses = list()
        for close, open in zip(close_data, open_data, strict=True):
            value = (close - open) / open
            if value > 0:
                gains.append(value)
            else:
                losses.append(value)
        self.average_gain = np.mean(gains)
        self.average_loss = np.mean(losses)


class StandardDeviation(BaseIndicator):
    def __init__(self, period: int, equity: str, cursor: sqlite3.Cursor) -> None:
        super(StandardDeviation, self).__init__(period, equity, cursor)
    def update_value(self, new_value=None):
        '''
        This is a convenience method that allows for an updated
        indicator value to be calculated without first creating
        and committing a transaction in the database to store the
        new data that will be used to calculate the indicator's
        new value.

        :param new_value: A new data point used to update the 
        indicator value.
        '''
        super().update_value(new_value=new_value)

class IndicatorController:
    def __init__(self, *indicators: BaseIndicator) -> None:
        self.indicators = [indicator for indicator in indicators]
    def update_indicators(self, new_values: list[float]) -> None:
        for indicator, value in zip(self.indicators, new_values, strict=True):
            indicator.update_value(value)