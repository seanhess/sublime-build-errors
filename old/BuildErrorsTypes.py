

class Completion(object):
    def __init__(self, dict):
        self.name = dict['name']
        self.type = dict['type']
        self.kind = dict['kind']
        self.full_symbol_name = dict['fullSymbolName']
        self.kind_modifiers = dict['kindModifiers']
        self.doc_comment = dict['docComment']

class Error(object):
    def __init__(self, dict):
        self.file = dict['file']
        self.text = dict['text']

        self.start = ErrorPosition(dict['start'])
        self.end = ErrorPosition(dict['end'])
        
        self.phase = dict['phase']
        self.category = dict['category']

class BuildError(object):
    def __init__(self, file, line, col, text):
        self.file = file
        self.text = text

        self.start = ErrorPosition({'line': line, 'character': col})
        self.end = ErrorPosition({'line': line, 'character': col+3})
        
        self.phase = None
        self.category = None

class ErrorPosition(object):
    def __init__(self, dict):
        self.line = dict['line']
        self.character = dict['character']    
