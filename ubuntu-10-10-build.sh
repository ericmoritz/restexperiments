# Get dependancies
apt-get -y update
apt-get -y install git varnish python-setuptools memcached apache2-utils python-dev build-essential

# Build libmemcached
mkdir src
pushd src
  curl http://launchpadlibrarian.net/56440579/libmemcached-0.44.tar.gz | tar xz
  pushd libmemcached-0.44
    ./configure && make install
    ldconfig
  popd
popd

# install the data-collation deps
pushd data-collation
  python setup.py develop
popd

# install the caching deps
pushd caching
  python setup.py develop
popd
