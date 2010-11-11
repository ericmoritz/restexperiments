import urllib

def GET(uri):
    fh = urllib.urlopen(uri)
    return fh.read()
