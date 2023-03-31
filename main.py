import jsonpickle
from typing import cast, Union
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from modules.NetworkCrawler import NetworkCrawler

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

credentialsMap = {}
defaultCredentials = {
    "user": "admin",
    "password": "admin",
    "secret": "cisco"
}

initialHost = "168.16.1.1"


@app.get("/start_crawl")
def startCrawl():
    crawler = NetworkCrawler(defaultCredentials, credentialsMap)
    crawler.crawl(initialHost, defaultCredentials)

    return {
        "devices": jsonpickle.encode(crawler.deviceMap, indent=4, unpicklable=False),
        "connections": jsonpickle.encode(crawler.connectionMap, indent=4, unpicklable=False)
    }


@app.get('/demo')
def demo():
    crawler = NetworkCrawler(defaultCredentials, credentialsMap)
    crawler.performScan(initialHost, None, defaultCredentials)
    devMap = cast(str, jsonpickle.encode(
        crawler.deviceMap, indent=4, unpicklable=False))
    connectionMap = cast(str, jsonpickle.encode(
        crawler.connectionMap, indent=4, unpicklable=False))
    response = '{"devices": ' + devMap + \
        ', "connections": ' + connectionMap + '}'

    return Response(content=response, media_type="application/json")
