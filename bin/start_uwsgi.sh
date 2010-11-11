./bin/uwsgi -s sock/uwsgi.sock -i -H `pwd`/ -M -p 4 -z 30 -l 500 -L  --module restexperiments.app
