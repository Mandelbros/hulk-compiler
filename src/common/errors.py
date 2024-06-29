

class HulkError(Exception):
    def __init__(self, text):
        super().__init__(text)

    @property
    def error_type(self):
        return 'HulkError'

    @property
    def text(self):
        return self.args[0]

    def __str__(self):
        return f'{self.error_type}: {self.text}'

    def __repr__(self):
        return str(self)

class HulkParserError(HulkError):
    def __init__(self, text, row, col):
        super().__init__(text)
        self.row = row
        self.col = col

    def __str__(self):
        return f'({self.row}, {self.col}) - {self.error_type}: {self.text}'

    PARSING_ERROR = 'Error at token \'%s\'.'

    @property
    def error_type(self):
        return 'ParserError'
    

class HulkLexerError(HulkError):            
    def __init__(self, text, row, col):
        super().__init__(text)
        self.row = row
        self.col = col

    def __str__(self):
        return f'({self.row}, {self.col}) - {self.error_type}: {self.text}'

    UNKNOWN_TOKEN = 'Unknown token \'%s\'.' 

    @property
    def error_type(self):
        return 'LexerError'
