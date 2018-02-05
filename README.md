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