class Script(object):

    def __init__(self, data):
    	contents = data['contents'][0]
    	line = int(data['line'][0])
    	column = int(data['column'][0])
    	startColumn = int(data['startColumn'][0])
    	filename = data['filename'][0]

        self.contents = contents.split("\n")
        self.line = line
        self.column = column
        self.startColumn = startColumn
        self.filename = filename

        self.tokens = set(contents.split())

        self.currentLine = self.contents[self.line].lstrip()
        self.previousLine = self.contents[self.line - 1].lstrip() if self.line > 0 else None