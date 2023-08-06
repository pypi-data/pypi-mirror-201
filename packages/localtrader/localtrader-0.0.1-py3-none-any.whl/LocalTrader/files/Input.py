
import re

class InFile:
    '''
    Base class used for operating on input files.
    '''
    def __init__(self, file: str) -> None:
        with open(file) as f:
            self.contents = f.read().strip()
            f.close()
    def read_file_contents(self, *patterns):
        '''
        Parses the input file for matches to the specified
        regular expression patterns and returns them as a list.

        :param patterns: Any number of regex patterns used to parse the input file.
        '''
        return [re.match(self.contents, pattern).group(0) for pattern in patterns]


class APIConfigFile(InFile):
    '''
    This class contains methods necessary to parse API
    details from a configuration file.
    '''
    def __init__(self, file: str) -> None:
        super().__init__(file)
        self.api_endpoint_regex = "(?<=api_endpoint=)[^ ]+"
        self.api_key_regex = "(?<=api_key=)[^ ]+"

    def read_file_contents(self) -> list[str]:
        '''
        Parses the contents of the input file for the user's 
        API endpoint and API key, which are returned as a list
        with the API endpoint in the 0-index position and the 
        API key in the 1st index.
        '''
        return super().read_file_contents(self.api_endpoint_regex, self.api_key_regex)
    
class WarmUpConfigFile(InFile):
    '''
    This class allows for the parsing of a configuration
    file used to specify warm-up procedures for the LocalTrader
    program.
    '''
    def __init__(self, file: str) -> None:
        super().__init__(file)
