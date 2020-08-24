# coding: utf-8

import os
import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

import gzip

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root)

import tenjin
from tenjin.helpers import *  # tenjin: this is ugly...

from git.commits_graph import generate_graph_data
from commit import Commit


engine = tenjin.Engine()


def app(environ, start_response):
    """ try
    http://localhost:8887
    http://localhost:8887/?{path}
    """
    status = '200 OK'
    headers = []
    path = environ['RAW_URI']
    [path, query] = (path.split('?') if '?' in path
                     else [path, None])
    if path.endswith('.js'):
        headers.append(('content-type', 'application/javascript'))
        start_response(status, headers)
        response_body = open('..' + path,'rb').read()
        return iter([response_body])
    headers.append(('content-type', 'text/html'))
    start_response(status, headers)
    data = generate_graph_data(Commit.gets(query or root))
    result = engine.render('index.html', {'data': data})
    return iter([result.encode('utf8')])
