ss:
	supervisord -c supervisord.conf -j ./run/supervisord.pid

ps:
	cat ./run/supervisord.pid | xargs kill

status:
	supervisorctl -c supervisord.conf status

st: status

build_env:
	mkdir log
	mkdir run
	mkdir -p data/export
	mkdir -p data/mongodb/inst1
	mkdir -p data/redis

req:
	pip install -r requirements.txt

init_data:
	python init.py

clean: clean_pyc clean_tmp
	@#@find -regex ".*\.\(pyc\|swp\|un\~\)" | xargs rm -rf

clean_pyc:
	@find `pwd` -name '*.pyc' -type f -delete

clean_tmp:
	@find `pwd` \( -name '*.swp' -o -name '*.un~' \) -type f -delete 
