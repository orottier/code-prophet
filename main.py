import sys
from Scanner import Scanner
from Prophet import Prophet
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse
import urllib
import json
import cgi

path = sys.argv[1]
pattern = sys.argv[2]
print "Traversing", path, "with pattern", pattern

scanner = Scanner(path, pattern)
fileDict = scanner.scan()

prophet = Prophet(fileDict)

#set up API
class RequestHandler(BaseHTTPRequestHandler):
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
		print postvars

		if parsed_path.path == '/heartbeat' :
			returnJson = {'status':  'ok'}
		elif parsed_path.path == '/completions':
			returnJson = prophet.speak(postvars)
		else:
			returnJson = {'error': 'command ' + parsed_path.path + ' does not exist'}

		self.wfile.write(json.dumps(returnJson, encoding = 'latin1'))

server = HTTPServer(('', 8080), RequestHandler)
print "API listening at port 8080"
server.serve_forever()
