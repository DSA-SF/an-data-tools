import logging
from pprint import pprint
import requests
import config
from ratelimit import limits

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class ActionNetworkClient:
    def __init__(self, an_api_key=config.AN_API_KEY):
        self.an_api_key = an_api_key

    @limit(calls=4, period=1)
    def get_member_list(self):
        DEBUG_MAX_PAGES = None
        DEBUG_MAX_PAGES = 4
        page = 1
        members = []
        while True:
            logging.info("Fetching people page %s", page)
            r = requests.get(
                f"https://actionnetwork.org/api/v2/people/?page={page}",
                headers={
                    "Content-Type": "application/json",
                    "OSDI-API-Token": self.an_api_key,
                },
            )
            result = r.json()

            if not result["_embedded"]["osdi:people"]:
                break

            members.extend(result["_embedded"]["osdi:people"])
            page += 1

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return members

if __name__ == '__main__':
    an_client = ActionNetworkClient()
    members = an_client.get_member_list()
    pprint(members)
