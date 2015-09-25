import operator
from itertools import ifilter
from Completion import LineCompletion, TokenCompletion, CompletionBuilder
from Script import Script

MIN_TOKEN_LENGTH = 4
MAX_COMPLETIONS = 10

class Prophet:

    def __init__(self, fileDict):

        """word separators for tokenizer: " ./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?",  """

        """ first line context """
        firstLines = {}
        for key,lines in fileDict.items():
            first = lines[0]
            if not first in firstLines:
                firstLines[first] = 0
            firstLines[first] += 1
        self.firstLines = sorted(firstLines.items(), key=operator.itemgetter(1), reverse=True)

        """ no context """
        allLines = {}
        for key,lines in fileDict.items():
            for line in lines:
                if len(line) >= MIN_TOKEN_LENGTH:
                    if not line in allLines:
                        allLines[line] = 0
                    allLines[line] += 1
        self.allLines = sorted(allLines.items(), key=operator.itemgetter(1), reverse=True)

        """ previous line context """
        prevLines = {}
        for key,lines in fileDict.items():
            prev = None;
            for line in lines:
                if prev:
                    if not prev in prevLines:
                        prevLines[prev] = {}
                    if not line in prevLines[prev]:
                        prevLines[prev][line] = 0
                    prevLines[prev][line] += 1
                prev = line
        for key,nextValues in prevLines.items():
            prevLines[key] = sorted(prevLines[key].items(), key=operator.itemgetter(1), reverse=True)
        self.prevLines = prevLines

    def completeLine(self, script, builder):
        line = script.currentLine
        offset = script.column - script.startColumn

        if script.previousLine and script.previousLine in self.prevLines:
            completions = [(complete[len(line) - offset:], 500*count) for (complete, count) in self.prevLines[script.previousLine] if line in complete]
            builder.addMany([LineCompletion(text, "ContPrev", count) for (text, count) in completions])

        completions = [(complete[len(line) - offset:], count) for (complete, count) in self.allLines if line in complete]
        builder.addMany([LineCompletion(text, "ContAll", count) for (text, count) in completions])


    def speak(self, script):
        completions = self.getCompletions(script)
        return completions

    def getCompletions(self, script):
        builder = CompletionBuilder(script.query, maxItems = MAX_COMPLETIONS, minTokenLength = MIN_TOKEN_LENGTH)

        # full line suggest for empty lines
        if not script.currentLine:
            # first line
            if script.line == 0:
                builder.addMany([LineCompletion(text, "1st", count) for (text, count) in self.firstLines])
            # previous line
            if script.previousLine and script.previousLine in self.prevLines:
                builder.addMany([LineCompletion(text, "Prev", 500*count) for (text, count) in self.prevLines[script.previousLine]])
            # general
            builder.addMany([LineCompletion(text, "All", count) for (text, count) in self.allLines])
        else:
            self.completeLine(script, builder)
            builder.addMany([TokenCompletion(text, "identifier") for text in script.tokens if text != script.query])

        return builder.getCompletions()

