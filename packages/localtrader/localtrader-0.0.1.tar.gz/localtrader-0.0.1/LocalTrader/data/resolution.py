'''
Contains all resolution types for market data. These
types represent varying periods of time whose data can
be encapsulated in synthetic constructs such as candle
objects.
'''

class Resolution:
    pass

class Daily(Resolution):
    pass

class Hourly(Resolution):
    pass

class Minute(Resolution):
    pass