# mavilla

Mavilla is a name inspired by a renowned Brazilian Historian Marco Antônio Villa. It is a system that acts like a historian, looking for references in sources recursively.


## How does it work:

First of all, you need to do a request through mavilla form, telling us which URL ("http://claudio-santos.com/") you want to investigate. Then our asynchronous process takes your request and starts to process, what means that a celery task will pick up your request, start the historian.task.investigate_it. Investigate_it task will read the URL through a process called scrape which uses the phantomJS headless browser that read the page, even if it has a JavaScript script and, gets all references. Then we record the URLs in a MongoDB Database and we call investigate_it task recursively.

Each time we get an URL, we send back to the website a WebSocket request to tell you (dear user) what we have been doing.

This 'simple' website use a few complex concepts like:
 - Websocket;
 - Asyncronous process;
 - Data Scrape;
 - Chains of async tasks;
 - Containers;

It's a great source of learning, so take a sit, get comfortable and enjoy.

## How to replicate the solution at your machine

1- Create the broker with RabbitMQ, and a MongoDB container to get some flexibility on Database Structure. Remember to change the <full_path_folder> to your file system path.

``` bash
	docker run -d --hostname rabbitmq -p 5672:5672 --name ibm-rabbitmq rabbitmq:3
	docker run --name ibm-mongo -p 27017:27017 -v <full_path_folder>/data:/data/db -d mongo
```

2- Get those machines IP addresses, which we just created.

```
	docker inspect ibm-mongo | grep IPAddress
	docker inspect ibm-rabbitmq | grep IPAddress
```

3- Then create the mahilla container which has the celery and the webserver

```
	docker run -d --hostname mavilla -p 5000:5000 -e "BROKER_HOST=<BROKER_DB_IP>" -e "WEBSERVER_HOST=localhost" -e "MONGO_HOST=<MONGO_DB_IP>" -e "WEBSERVER_PORT=5000" -e "MONGO_PORT=27017" --link ibm-mongo --link ibm-rabbitmq --name mavilla simplologia/mavilla:latest
```

4- Go to your web browser and access the [http://localhost:5000/](http://localhost:5000/), type the website which you want to investigate as follows http://claudio-santos.com/.




