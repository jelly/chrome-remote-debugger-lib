import json
import sys

import requests
import websocket

class ChromeDebuggerConnectionError(Exception):
    pass

class ChromeShell(object):
    def __init__(self, host='localhost', port=9222):
        self.host = host
        self.port = port
        self.url = 'http://{0}:{1}/json/'.format(self.host, self.port)

    def tabs(self, title=''):
        try:
            tabs = json.loads(requests.get(self.url + 'list').text)
        except requests.ConnectionError:
            raise ChromeDebuggerConnectionError('Unable to connect to Chrome debugger on {0}'.format(self.url))

        return [ChromeTab(tab, self) for tab in tabs if title in tab['title']]

    def create_tab(self, url = None):
        if url:
            url = self.url + 'new?' + url
        else:
            url = self.url + 'new'

        req = requests.get(url)
        return ChromeTab(json.loads(req.text), shell=self)

    def __repr__(self):
        return 'ChromiumShell(host={0}, port={1})'.format(self.host, self.port)

class ChromeTab(object):
    def __init__(self, data, shell):
        self.shell = shell
        self.data = data
        self.cmd_id = 1
        self._ws = None # Lazy load websocket url


    @property
    def id(self):
        return self.data['id']

    @property
    def title(self):
        return self.data['title']

    @property
    def ws(self):
        # XXX: where do we close the websocket?
        if self._ws is None:
            self._ws = websocket.create_connection(self.data['webSocketDebuggerUrl'])
        return self._ws

    def close(self):
        req = requests.get(self.shell.url + 'close/' + self.id)
        # XXX: or raise exception?
        if 'Could not close' in req.text:
            return False
        else:
            return True

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

    def navigate(self, url):
        # XXX: wrapper for generating payload + request
        payload = { 'id': self.cmd_id, 'method': 'Page.navigate', 'params': {'url': url}}
        self.ws.send(json.dumps(payload)) # XXX: exceptions
        self.cmd_id += 1

        data = json.loads(self.ws.recv())
        # FIXME: resolve to new tab instance.
        print data
        # XXX: update tab


    def __unicode__(self):
        # XXX: empty title
        return u'ChromiumTab({0})'.format(self.data['title'])

    def __repr__(self):
        return unicode(self).encode(sys.stdout.encoding or 'utf8')
