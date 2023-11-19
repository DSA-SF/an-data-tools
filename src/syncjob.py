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
