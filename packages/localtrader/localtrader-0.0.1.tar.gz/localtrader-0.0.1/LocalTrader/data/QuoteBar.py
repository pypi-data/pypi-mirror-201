'''
Contains the `QuoteBar` class, which is used to interact
with live price quotes for a specified equity.
'''

class QuoteBar:
    '''
    Represents live price quotes for an equity.
    '''
    def __init__(self, quote: float) -> None:
        self.quote = quote
    def getQuote(self) -> float:
        return self.quote