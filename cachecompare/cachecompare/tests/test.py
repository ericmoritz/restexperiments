import sys
from multiprocessing import Process
import time
import os
import logging
import subprocess
import urllib
import unittest


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
results_path = "./results"
here = os.path.abspath(os.path.dirname(__file__))
apps_dir = os.path.join(here, "../apps")


assert os.path.isdir(results_path), ("Create a directory called results in"
                                     " your current working directory")
def app(filename):
    """Return a path in the apps dir"""
    return os.path.join(apps_dir, filename)

def rp(filename):
    """Returns the results path to the file"""
    return os.path.join(results_path, filename)


def runcommand(cmd):
    """Returns the output of a command"""
    p = subprocess.Popen(cmd, shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    errors = p.stderr.read()
    result = p.stdout.read()
    ret = p.wait()

    if ret != 0:
        raise Exception(errors)

    return result


def runserver(server_script):
    server_script = os.path.abspath(server_script)
    execfile(server_script,
             {'__file__': server_script,
              '__name__': '__main__'})


def abtest(url):
    result = runcommand('ab -n 1000 -c 1 %s' % url)
    return result


class BaseAppTestCase(object):
    ignore = False

    def test_primed(self):
        testname = self.testname
        server_script = self.server_script
        uri = self.uri

        if(self.ignore):
            log.info("%s test ignored" % (testname, ))
            return

        server = Process(target=runserver, args=(server_script, ))
        log.info("Starting the %s server" % (testname, ))
        server.start()

        # wait for everything to come up
        log.info("Waiting 1 second for the server to come up")
        time.sleep(1)

        log.info("Priming the cache and storing the result (for debugging)")
        content = urllib.urlopen(uri).read()
        print >> sys.stderr, content        
        with open(rp("%s.html" % (testname, )), "w") as fh:
            fh.write(content)

        log.info("Running Apache Bench on %s" % (uri, ))
        primed = abtest(uri)
        print >> sys.stderr, primed
        
        log.info("Shutting down the %s server" % (testname, ))
        server.terminate()
        log.info("Waiting 1 second for the server to die")
        time.sleep(1)

        result_filename = rp("%s.ab.txt" % (testname, ))

        with open(result_filename, "w") as fh:
            fh.write(primed)

class ControlTest(BaseAppTestCase, unittest.TestCase):
    testname = "control"
    uri = "http://localhost:8000/"
    server_script = app("control/app.py")


class LocMemTest(BaseAppTestCase, unittest.TestCase):
    testname = "locmem"
    uri = "http://localhost:8000/"
    server_script = app("locmem/app.py")


class MemcacheTest(BaseAppTestCase, unittest.TestCase):
    testname = "memcache"
    uri = "http://localhost:8000/"
    server_script = app("memcache/app.py")


class MiddlewareTest(BaseAppTestCase, unittest.TestCase):
    testname = "middleware"
    uri = "http://localhost:8000/"
    server_script = app("middleware/app.py")


class VarnishTest(BaseAppTestCase, unittest.TestCase):
    testname = "varnish"
    uri = "http://localhost:10001/"
    server_script = app("middleware/app.py")


if __name__ == '__main__':
    unittest.main()
