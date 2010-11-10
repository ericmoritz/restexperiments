# Get dependancies
apt-get -y update
apt-get -y install git varnish python-setuptools memcached apache2-utils python-dev build-essential python-software-properties libxml2-dev nginx libpcre3 libpcre3-dev

# Build libmemcached
mkdir src
pushd src
  curl http://launchpadlibrarian.net/56440579/libmemcached-0.44.tar.gz | tar xz
  pushd libmemcached-0.44
    ./configure && make install
    ldconfig
  popd
popd

# Build uwsgi
pushd src
  curl http://projects.unbit.it/downloads/uwsgi-0.9.6.5.tar.gz | tar xz
  pushd uwsgi-0.9.6.5
    make
    cp uwsgi ../../bin
  popd
popd

# Build nginx
pushd src
  curl http://nginx.org/download/nginx-0.8.53.tar.gz | tar xz
  pushd nginx-0.8.53
    ./configure
    make
    cp objs/nginx ../../bin
  popd
popd

# install the python deps
python setup.py develop
