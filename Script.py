class Script(object):

    def __init__(self, data):
    	contents = data['contents'][0]
    	line = int(data['line'][0])
    	column = int(data['column'][0])
    	startColumn = int(data['startColumn'][0])
    	filename = data['filename'][0]
    	query = data['query'][0]

        self.contents = contents.split("\n")
        self.line = line
        self.column = column
        self.startColumn = startColumn
        self.filename = filename

        # split file by whitespace, can be more intelligent
        self.tokens = set(contents.split())

        self.currentLine = self.contents[self.line].lstrip()

        # find the previous, non blank line
        previousLine = None
        lineBack = 0
        while self.line - lineBack > 0 and not previousLine:
        	lineBack += 1
        	previousLine = self.contents[self.line - lineBack].lstrip()
        self.previousLine = previousLine

        # the text that is already typed, used to filter the completions
        self.query = self.contents[self.line][startColumn:column] # do not strip the whitespace
        self.query = query # always identical?

    def display(self):
    	print "Script: ", self.filename
    	print "Line", self.line, "Column", self.column, "StartColumn", self.startColumn
    	print "Current Line: ", self.currentLine
    	print "Previous Line: ", self.previousLine
    	print "Query: ", self.query
    	print