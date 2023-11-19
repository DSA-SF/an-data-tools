from pprint import pprint
from dateutil import parser
from first import first
from sqlalchemy import insert, select
import db
import config
from anclient import ActionNetworkClient


def sync_an_people_to_db(an: ActionNetworkClient, Session: db.Session):
    members = an.get_member_list()

    with Session() as session:
        session.execute(
            insert(db.Member),
            [
                {
                    "action_network_id": member["identifiers"][0].split(":")[-1],
                    "first_name": member.get("given_name"),
                    "last_name": member.get("family_name"),
                    "email": first(
                        member["email_addresses"], key=lambda x: x["primary"]
                    )["address"],
                }
                for member in members
            ],
        )
        session.commit()


def sync_an_actions_to_db(an: ActionNetworkClient, Session: db.Session):
    actions = an.get_action_list()

    with Session() as session:
        records = [
            {
                "action_network_id": action["identifiers"][0].split(":")[-1],
                "title": action.get("title"),
                "description": action.get("description"),
                "created_ts": "created_date" in action
                and parser.parse(action["created_date"]),
                "modified_ts": "modified_date" in action
                and parser.parse(action["modified_date"]),
                "browser_url": action.get("browser_url"),
                "start_ts": "start_date" in action
                and parser.parse(action["start_date"]),
                "location": action.get("location")
                and action["location"].get("venue")
                or None,
            }
            for action in actions
        ]
        session.execute(insert(db.Action), records)
        session.commit()


def sync_an_tags_to_db(an: ActionNetworkClient, Session: db.Session):
    tags = an.get_tag_list()

    with Session() as session:
        session.execute(
            insert(db.Tag),
            [
                {
                    "action_network_id": tag["identifiers"][0].split(":")[-1],
                    "name": tag.get("name"),
                }
                for tag in tags
            ],
        )
        session.commit()


def sync_an_taggings_to_db(an: ActionNetworkClient, Session: db.Session):
    with Session() as session:
        all_tag_ids = session.execute(
            select(db.Tag.action_network_id)
        ).fetchall()

        DEBUG_MAX_TAGS_TO_FETCH = 1 if config.DEV_MODE else None
        tags_fetched = 0

        taggings = []
        tag_ids = set([tag_id[0] for tag_id in all_tag_ids])
        for tag_id in tag_ids:
            taggings.extend(an.get_tagging_list(tag_id))
            tags_fetched += 1
            if DEBUG_MAX_TAGS_TO_FETCH and tags_fetched >= DEBUG_MAX_TAGS_TO_FETCH:
                break

        session.execute(
            insert(db.Tagging),
            [
                {
                    "action_network_id": tagging["_links"]["self"]["href"].split("/")[-1],
                    "member_action_network_id": tagging["_links"]["osdi:person"][
                        "href"
                    ].split("/")[-1],
                    "tag_action_network_id": tagging["_links"]["osdi:tag"][
                        "href"
                    ].split("/")[-1],
                    "created_ts": "created_date" in tagging
                    and parser.parse(tagging["created_date"]),
                    "modified_ts": "modified_date" in tagging
                    and parser.parse(tagging["modified_date"]),
                }
                for tagging in taggings
            ],
        )
        session.commit()


def sync_an_attendances_to_db(an: ActionNetworkClient, Session: db.Session):
    with Session() as session:
        all_event_ids = session.execute(
            select(db.Action.action_network_id)
        ).fetchall()

        DEBUG_MAX_EVENTS_TO_FETCH = 1 if config.DEV_MODE else None
        events_fetched = 0

        attendances = []
        event_ids = set([event_id[0] for event_id in all_event_ids])
        for event_id in event_ids:
            attendances.extend(an.get_attendance_list(event_id))
            events_fetched += 1
            if DEBUG_MAX_EVENTS_TO_FETCH and events_fetched >= DEBUG_MAX_EVENTS_TO_FETCH:
                break

        session.execute(
            insert(db.Attendance),
            [
                {
                    "action_network_id": attendance["identifiers"][0].split(":")[-1],
                    "member_action_network_id": attendance["_links"]["osdi:person"][
                        "href"
                    ].split("/")[-1],
                    "action_action_network_id": attendance["_links"]["osdi:event"][
                        "href"
                    ].split("/")[-1],
                    "created_ts": "created_date" in attendance
                    and parser.parse(attendance["created_date"]),
                }
                for attendance in attendances
            ],
        )
        session.commit()
