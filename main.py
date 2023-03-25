import jsonpickle
from typing import cast
from modules.NetworkCrawler import NetworkCrawler


credentialsMap = {}
defaultCredentials = {
    "user": "admin",
    "password": "admin",
    "secret": "cisco"
}

initialHost = "168.16.1.1"

crawler = NetworkCrawler(defaultCredentials, credentialsMap)
crawler.crawl(initialHost, defaultCredentials)

print(jsonpickle.encode(crawler.deviceMap, indent=4, unpicklable=False))
print(jsonpickle.encode(crawler.connectionMap, indent=4, unpicklable=False))
