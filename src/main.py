import db
from anclient import ActionNetworkClient
from syncjob import (
    sync_an_attendances_to_db,
    sync_an_people_to_db,
    sync_an_actions_to_db,
    sync_an_taggings_to_db,
    sync_an_tags_to_db,
)
from views import create_views


def main():
    an = ActionNetworkClient()
    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)
    sync_an_people_to_db(an, db.Session)
    sync_an_tags_to_db(an, db.Session)
    sync_an_taggings_to_db(an, db.Session)
    sync_an_actions_to_db(an, db.Session)
    sync_an_attendances_to_db(an, db.Session)

    create_views(db.engine)

if __name__ == "__main__":
    main()
