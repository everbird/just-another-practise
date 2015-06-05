ss:
	supervisord -c supervisord.conf -j ./run/supervisord.pid

ps:
	cat ./run/supervisord.pid | xargs kill

status:
	supervisorctl -c supervisord.conf status

st: status
