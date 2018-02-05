docker run -d --hostname rabbitmq -p 5672:5672 --name ibm-rabbitmq rabbitmq:3
docker run --name ibm-mongo -p 27017:27017 -v /home/claudio/projects/csantos/ibm-challenge/data:/data/db -d mongo

docker inspect ibm-mongo | grep IPAddress
docker inspect ibm-rabbitmq | grep IPAddress

docker run -d --hostname mavilla -p 5000:5000 -e "BROKER_HOST=172.17.0.2" -e "WEBSERVER_HOST=localhost" -e "MONGO_HOST=172.17.0.3" -e "WEBSERVER_PORT=5000" -e "MONGO_PORT=27017" --link ibm-mongo --link ibm-rabbitmq --name mavilla simplologia/mavilla:latest

python -m unittest discover -s historian/tests/ -v

investigate_from.delay('http://claudio-santos.com')

celery -A website worker -l info


from historian.investigation import Investigation
investigation = Investigation('http://claudio-santos.com/')
investigation.investigate_unprocessed_url(investigation.unprocessed_urls())

investigation.db._client.drop_database('ibm')



from historian.tasks.investigate import investigate
result = investigate.delay('http://claudio-santos.com/')


from pymongo import MongoClient
_client = MongoClient('mongodb://{0}:{0}}/'.format(os.environ['MONGO_HOST'],os.environ['MONGO_PORT']))
db = _client['ibm']
db.list_collections()
_client.drop_database('ibm')

collection =  '3ce5bf8f-5e4d-4b9f-8877-c73a6f4c8793' #'3b22ca39-f19e-4a39-bd18-ed927cb7a246' # d332f961-f843-46a6-84a5-ee7f477ebdc0'

from pymongo import MongoClient
def list_them_all(collection):
    _client = MongoClient('mongodb://localhost:27017/')
    _database = _client['ibm']
    db = _database[collection]
    cursor = db.find()
    count = 0
    for item in cursor:
        print(item['child_task_id'], item['parent'], item['url'], item['processed'])
        count += 1
    print(count)

def kill_them_all(collection):
    from historian.celery import app
    _client = MongoClient('mongodb://localhost:27017/')
    _database = _client['ibm']
    db = _database[collection]
    cursor = db.find()
    for item in cursor:
        print(item['child_task_id'], item['url'])
        result = app.AsyncResult(item['child_task_id'])
        result.revoke()


from website.celery import app
result = app.AsyncResult('858e40ee-80d8-4363-a395-82cabfb130ce')
while True:
    result.revoke(terminate=True)
    result = app.AsyncResult(result.get())
    print(result.get())    



print(result.get())    
result = app.AsyncResult(result.get())
if not result.ready():
result.revoke()
break


class MessageNamespace(BaseNamespace):
    def on_aaa_response(self, *args):
        print('on_aaa_response', args)


from socketIO_client import SocketIO, BaseNamespace
socketIO = SocketIO('localhost', 5000)
message_namespace = socketIO.define(BaseNamespace, '/msg')
message_namespace.emit('message_sent', {'data':'hello websocket'})
socketIO.wait(seconds=1)


from socketIO_client import SocketIO
socketIO = SocketIO('localhost', 5000)
socketIO.emit('sendMessage', {'data': 'Processing {0}'.format('url')})
