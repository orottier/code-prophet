import sys
from Scanner import Scanner
from Prophet import Prophet
from Script import Script
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
import urllib
import json
import cgi
import argparse

parser = argparse.ArgumentParser(description='Fire up the Prophet code autocompleter API')
parser.add_argument('path', help='root directory of code')
parser.add_argument('pattern', help='source files should match this pattern')

args = parser.parse_args()
path = args.path
pattern = args.pattern

print "Traversing", path, "with pattern", pattern
scanner = Scanner(path, pattern)
fileDict = scanner.scan()
print scanner.files, "files, with", scanner.lines, "non blank lines"

prophet = Prophet(fileDict)

#set up API
class RequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)
		self.wfile.write("<h1>Prophet code completer</h1> path: " + path + "<br> pattern: " + pattern)

	def do_POST(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()

		parsed_path = urlparse.urlparse(self.path)
		params = urlparse.parse_qs(parsed_path.query)

		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
			postvars = {}

		print parsed_path

		if parsed_path.path == '/heartbeat' :
			returnJson = {'status':  'ok'}
		elif parsed_path.path == '/completions':
			script = Script(postvars)
			script.display()
			returnJson = prophet.speak(script)
		else:
			returnJson = {'error': 'command ' + parsed_path.path + ' does not exist'}

		print "Returning", len(returnJson), "items"
		print
		self.wfile.write(json.dumps(returnJson, encoding = 'latin1'))

server = HTTPServer(('', 8080), RequestHandler)
print "API listening at port 8080"
print
server.serve_forever()
