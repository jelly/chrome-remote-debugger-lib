import json
import sys

import requests
import websocket

class ChromeShell(object):
    def __init__(self, host='localhost', port=9222):
        self.host = host
        self.port = port

    def tabs(self):
        # FIXME: Exception

        tabs = json.loads(requests.get('http://{0}:{1}/json'.format(self.host, self.port)).text)
        return [ChromeTab(tab) for tab in tabs]

    def __repr__(self):
        return 'ChromiumShell(host={0}, port={1})'.format(self.host, self.port)

class ChromeTab(object):
    def __init__(self, data):
        self.data = data
        self.cmd_id = 1
        self._ws = None # Lazy load websocket url

    @property
    def ws(self):
        # XXX: where do we close the websocket?
        if self._ws is None:
            self._ws = websocket.create_connection(self.data['webSocketDebuggerUrl'])
        return self._ws

    def reload(self, cache=True, script=''):
        # XXX: check if script is sane?
        payload = { 'id': self.cmd_id, 'method': 'Page.reload', 'params': {'ignoreCache': cache, 'scriptToEvaluateOnLoad': script}}
        self.ws.send(json.dumps(payload)) # XXX: exceptions
        self.cmd_id += 1

        data = json.loads(self.ws.recv())
        # FIXME: more error handling?
        if 'errors' in data:
            return False
        else:
            return True


    def __unicode__(self):
        return u'ChromiumTab({0})'.format(self.data['title'])

    def __repr__(self):
        return unicode(self).encode(sys.stdout.encoding or 'utf8')
