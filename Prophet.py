import operator
from itertools import ifilter
from Completion import Completion
from Script import Script

MIN_LENGTH = 4

class Prophet:

    def __init__(self, fileDict):

        """word separators for tokenizer: " ./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?",  """

        """ first line context """
        firstLines = {}
        for key,lines in fileDict.items():
            first = lines[0]
            if not first in firstLines:
                firstLines[first] = 0
            firstLines[first] += 1./len(first)
        self.firstLines = sorted(firstLines.items(), key=operator.itemgetter(1), reverse=True)

        """ no context """
        allLines = {}
        for key,lines in fileDict.items():
            for line in lines:
                if len(line) >= MIN_LENGTH:
                    if not line in allLines:
                        allLines[line] = 0
                    allLines[line] += 1./len(line)
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
                    prevLines[prev][line] += 1./len(line)
                prev = line
        for key,nextValues in prevLines.items():
            prevLines[key] = sorted(prevLines[key].items(), key=operator.itemgetter(1), reverse=True)
        self.prevLines = prevLines

    def completeLine(self, script):
        line = script.currentLine
        offset = script.column - script.startColumn
        return [(complete[len(line) - offset:], count) for (complete, count) in self.allLines if complete.startswith(line)]


    def speak(self, script):
        completions = []

        # full line suggest for empty lines
        if not script.currentLine:
            # first line
            if script.line == 0:
                completions += [Completion(text, "1st: " + str(count)).toJson() for (text, count) in self.firstLines]
            # previous line
            if script.previousLine and script.previousLine in self.prevLines:
                completions += [Completion(text, "Prev: " + str(count)).toJson() for (text, count) in self.prevLines[script.previousLine]]
            # general
            completions += [Completion(text, "All: " + str(count)).toJson() for (text, count) in self.allLines]
        else:
            lineContinuations = self.completeLine(script)
            if lineContinuations:
                completions += [Completion(text, "Cont: " + str(count)).toJson() for (text, count) in lineContinuations]
            completions += [Completion(text, "identifier").toJson() for text in script.tokens if text != script.query]

        return completions

