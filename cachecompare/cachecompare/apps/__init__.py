# Store the paths to the app files so that we can load them in a different
# process and in isolation
from cachecompare.apps.control import app
control_script = app.__file__.replace("pyc", "py")

from cachecompare.apps.locmem import app
locmem_script = app.__file__.replace("pyc", "py")

from cachecompare.apps.memcache import app as memcache_app
from cachecompare.apps.middleware import app as middleware_app
from cachecompare.apps.varnish import app as varnish_app

