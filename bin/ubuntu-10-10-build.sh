# Get system dependancies
apt-get -y update
apt-get -y install git varnish python-setuptools memcached apache2-utils python-dev build-essential python-software-properties libxml2-dev nginx libpcre3 libpcre3-dev

# install virtualenv
easy_install virtualenv

# Create a new environment
virtualenv .


# Install uwsgi
./bin/pip -E . install http://projects.unbit.it/downloads/uwsgi-latest.tar.gz

# Install the latest nginx
mkdir src

pushd src
   curl http://nginx.org/download/nginx-0.8.53.tar.gz | tar xz
   pushd nginx-0.8.53
     ./configure
     make
     cp objs/nginx ../../bin/
     cp conf/* ../../conf/
   popd
popd

# Deploy the rest test nginx conf
pushd conf
  rm nginx.conf
  ln -s nginx-resttest.conf nginx.conf
popd

# make the needed dirs for nginx
mkdir tmp/ sock/ pid/ logs/

# install the python deps
python setup.py develop
