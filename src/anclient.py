import logging
from pprint import pprint
import requests
from apicache import persist_to_file
import config
from ratelimit import limits, sleep_and_retry

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


class ActionNetworkClient:
    def __init__(self, an_api_key=config.AN_API_KEY):
        self.an_api_key = an_api_key

    @persist_to_file('memberlist.json')
    def get_member_list(self):
        DEBUG_MAX_PAGES = 1 if config.DEV_MODE else None
        page = 1
        members = []
        while True:
            logging.info("Fetching people page %s", page)
            result = self._do_get(
                f"https://actionnetwork.org/api/v2/people/?page={page}"
            )

            if not result["_embedded"]["osdi:people"]:
                break

            members.extend(result["_embedded"]["osdi:people"])
            page += 1

            # pprint(result["_embedded"]["osdi:people"])
            # print("\n\n\n")

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return members

    def get_action_list(self):
        DEBUG_MAX_PAGES = 1 if config.DEV_MODE else None
        page = 1
        actions = []
        while True:
            logging.info("Fetching events page %s", page)
            result = self._do_get(
                f"https://actionnetwork.org/api/v2/events/?page={page}"
            )

            if not result["_embedded"]["osdi:events"]:
                break

            actions.extend(result["_embedded"]["osdi:events"])
            page += 1

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return actions

    def get_attendance_list(self, event_id):
        DEBUG_MAX_PAGES = 1 if config.DEV_MODE else None
        page = 1
        attendances = []
        while True:
            logging.info("Fetching attendance for event %s page %s", event_id, page)
            result = self._do_get(
                f"https://actionnetwork.org/api/v2/events/{event_id}/attendances/?page={page}"
            )

            if not result["_embedded"]["osdi:attendances"]:
                break

            # AN API sometimes returns bogus attendances. We have to re-query for the specific one and see if it 404s.
            for attendance in result["_embedded"]["osdi:attendances"]:
                person_url = attendance["_links"]["osdi:person"]["href"]
                person_result = self._do_get(person_url)
                if "error" in person_result:
                    continue
                attendances.append(attendance)
            page += 1

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return attendances

    def get_tag_list(self):
        DEBUG_MAX_PAGES = 1 if config.DEV_MODE else None
        page = 1
        tags = []
        while True:
            logging.info("Fetching tags page %s", page)
            result = self._do_get(f"https://actionnetwork.org/api/v2/tags/?page={page}")

            if not result["_embedded"]["osdi:tags"]:
                break

            tags.extend(result["_embedded"]["osdi:tags"])
            page += 1

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return tags

    def get_tagging_list(self, tag_id):
        DEBUG_MAX_PAGES = 1 if config.DEV_MODE else None
        page = 1
        taggings = []
        while True:
            logging.info("Fetching taggings for tag %s page %s", tag_id, page)
            result = self._do_get(
                f"https://actionnetwork.org/api/v2/tags/{tag_id}/taggings/?page={page}"
            )

            if not result["_embedded"]["osdi:taggings"]:
                break

            taggings.extend(result["_embedded"]["osdi:taggings"])
            page += 1

            if DEBUG_MAX_PAGES and page > DEBUG_MAX_PAGES:
                break

        return taggings

    @sleep_and_retry
    @limits(calls=4, period=1)
    def _do_get(self, url):
        r = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "OSDI-API-Token": self.an_api_key,
            },
        )
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:
            logging.error("Failed to decode JSON response to %s: %s", url, r.text)
            raise


if __name__ == "__main__":
    an_client = ActionNetworkClient()
    members = an_client.get_member_list()
    pprint(members)
