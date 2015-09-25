class Script(object):

    def __init__(self, contents, line, column, filename):
        self.contents = contents
        self.line = line
        self.column = column
        self.filename = filename