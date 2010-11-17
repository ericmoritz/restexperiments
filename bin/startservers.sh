. ./bin/enable_highconcurrency.sh
./bin/nginx -p .
./bin/start_varnish.sh
./bin/start_uwsgi.sh