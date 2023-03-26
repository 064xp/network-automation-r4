import jsonpickle
from typing import cast, Union
from fastapi import FastAPI

from modules.NetworkCrawler import NetworkCrawler

app = FastAPI()

credentialsMap = {}
defaultCredentials = {
    "user": "admin",
    "password": "admin",
    "secret": "cisco"
}

initialHost = "168.16.1.1"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/start_crawl")
def startCrawl():
    crawler = NetworkCrawler(defaultCredentials, credentialsMap)
    crawler.crawl(initialHost, defaultCredentials)

    return {
        "devices": jsonpickle.encode(crawler.deviceMap, indent=4, unpicklable=False),
        "connections": jsonpickle.encode(crawler.connectionMap, indent=4, unpicklable=False)
    }


startCrawl()
