from ycmd.utils import ToUtf8IfNeeded
from ycmd.completers.completer import Completer
from ycmd import responses

import json
import requests
import urlparse

class ProphetCompleter( Completer ):
  """
  A Completer that uses the Prophet completion engine.
  """

  def __init__( self, user_options ):
      super( ProphetCompleter, self ).__init__( user_options )
      self.enabled = False
      result = self._Request('heartbeat')
      if 'status' in result and result['status'] == 'ok':
        self.enabled = True

  def _Request(self, path, parameters = {'nop': "nop"}):
      serverLocation = 'http://localhost:8080/'
      timeout = .2
      target = urlparse.urljoin( serverLocation, path )
      response = requests.post( target, data = parameters, timeout = timeout )
      return response.json()

  def SupportedFiletypes( self ):
      """ Just python """
      return [ 'python' ]

  def ShouldUseNow( self, request_data ):
      """ disable caching """
      self._completions_cache.Invalidate()
      """ Alway suggest completions, not only on triggers """
      return self.enabled

  def _GetScript( self, request_data ):
      filename = request_data[ 'filepath' ]
      contents = request_data[ 'file_data' ][ filename ][ 'contents' ]
      # 0 based lines/columns
      line = request_data[ 'line_num' ] - 1
      column = request_data[ 'column_num' ] - 1
      startColumn = request_data[ 'start_column' ] - 1
      query = request_data[ 'query' ]

      return {
        'contents': contents,
        'line': line,
        'column': column,
        'startColumn': startColumn,
        'filename': filename,
        'query': query
      }


  def _GetExtraData( self, completion ):
      location = {}
      if completion['module_path']:
        location[ 'filepath' ] = ToUtf8IfNeeded( completion['module_path'] )
      if completion['line']:
        location[ 'line_num' ] = completion['line']
      if completion['column']:
        location[ 'column_num' ] = completion['column'] + 1

      if location:
        extra_data = {}
        extra_data[ 'location' ] = location
        return extra_data
      else:
        return None


  def ComputeCandidatesInner( self, request_data ):
    script = self._GetScript( request_data )
    completions = self._Request('completions', script)
    return [ responses.BuildCompletionData(
                ToUtf8IfNeeded( completion['name'] ),
                ToUtf8IfNeeded( completion['description'] ),
                ToUtf8IfNeeded( completion['docstring'] ),
                extra_data = self._GetExtraData( completion ) )
             for completion in completions]

  def DefinedSubcommands( self ):
    return []
