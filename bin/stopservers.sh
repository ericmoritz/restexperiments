kill -int `cat pid/uwsgi.pid`
kill -int `cat pid/nginx.pid`
killall varnishd