import urllib

def GET(uri):
    with urllib.urlopen(uri) as fh:
        return fh.read()
