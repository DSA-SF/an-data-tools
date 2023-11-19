import logging
from pprint import pprint
import requests
import config
from ratelimit import limits

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class ActionNetworkClient:
    def __init__(self, an_api_key=config.AN_API_KEY):
        self.an_api_key = an_api_key

    def get_member_list(self):
        DEBUG_MAX_PAGES = 1 if config.DEV_MODE else None
        page = 1
        members = []
        while True:
            logging.info("Fetching people page %s", page)
            result = self._do_get(f"https://actionnetwork.org/api/v2/people/?page={page}")

            if not result["_embedded"]["osdi:people"]:
                break

            members.extend(result["_embedded"]["osdi:people"])
            page += 1

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return members
    
    def get_event_list(self):
        DEBUG_MAX_PAGES = 1 if config.DEV_MODE else None
        page = 1
        events = []
        while True:
            logging.info("Fetching events page %s", page)
            result = self._do_get(f"https://actionnetwork.org/api/v2/events/?page={page}")

            if not result["_embedded"]["osdi:events"]:
                break

            events.extend(result["_embedded"]["osdi:events"])
            page += 1

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return events

    @limits(calls=4, period=1)
    def _do_get(self, url):
        r = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "OSDI-API-Token": self.an_api_key,
            },
        )
        return r.json()

if __name__ == '__main__':
    an_client = ActionNetworkClient()
    members = an_client.get_member_list()
    pprint(members)
