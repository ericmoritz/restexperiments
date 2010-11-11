if [ -e pid/uwsgi.pid ]; then
    echo "Existing uwsgi, killing it."
    kill -int `cat pid/uwsgi.pid`
    sleep 0.5
fi

./bin/uwsgi --pidfile pid/uwsgi.pid -s sock/uwsgi.sock -i -H `pwd`/ -t 5 -M -p 4 -z 30 -l 500 -L  --module restexperiments.app