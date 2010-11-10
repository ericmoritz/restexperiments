# Get dependancies
add-apt-repository ppa:stevecrozz/ppa # for uwsgi
apt-get -y update
apt-get -y install nginx git varnish python-setuptools memcached apache2-utils python-dev build-essential

# Create a new virtual env
easy_install virtualenv
rm -rf env
virtualenv env --no-site-packages
. env/bin/activate

# Build libmemcached
mkdir src
pushd src
  curl http://launchpadlibrarian.net/56440579/libmemcached-0.44.tar.gz | tar xz
  pushd libmemcached-0.44
    ./configure && make install
    ldconfig
  popd
popd

# install the python deps
python setup.py develop
