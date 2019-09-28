if [ ! -d env ]; 
then 
	python -m venv env
fi



env/bin/activate
python server.py api.seraphim.online 20013 e18fd2e9cfa91559a9658bfe31e95160da755368f8e281b52945c6be48f3fdd7
