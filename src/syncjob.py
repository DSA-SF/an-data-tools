from pprint import pprint
from first import first
from sqlalchemy import insert
import db
from anclient import ActionNetworkClient

def sync_an_people_to_db(an: ActionNetworkClient, Session: db.Session):
    members = an.get_member_list()
    # bulk insert members into Member table

    pprint(members)
    with Session() as session:
        session.execute(insert(db.Member), 
            [
                {
                    "action_network_id": member["identifiers"][0],
                    "first_name": member.get("given_name"),
                    "last_name": member.get("family_name"),
                    "email": first(member["email_addresses"], key=lambda x: x["primary"])["address"],
                }
                for member in members
            ]
        )
        session.commit()

def sync_an_actions_to_db(an: ActionNetworkClient, Session: db.Session):
    actions = an.get_event_list()
    # bulk insert actions into Action table

    # pprint(actions)
    with Session() as session:
        records = [
                {
                    "action_network_id": action["identifiers"][0],
                    "title": action.get("title"),
                    "description": action.get("description"),
                    "created_date_iso": action.get("created_date"),
                    "modified_date_iso": action.get("modified_date"),
                    "browser_url": action.get("browser_url"),
                    "start_date_iso": action.get("start_date"),
                    "location": action.get("location") and action["location"].get("venue") or None,
                }
                for action in actions
            ]
        pprint(records)
        session.execute(insert(db.Action), 
            records
        )
        session.commit()
