# Get dependancies
apt-get -y update
apt-get -y install git varnish python-setuptools memcached apache2-utils

# Build libmemcached
mkdir src
pushd src
  curl http://launchpad.net/libmemcached/1.0/0.44/+download/libmemcached-0.44.tar.gz | tar xz
  pushd libmemcached-0.44
    ./configure && make install
  popd
popd

# install the data-collation deps
pushd data-collation
  python setup.py develop
popd
