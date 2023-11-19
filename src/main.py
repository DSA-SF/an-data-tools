import db
from anclient import ActionNetworkClient
from syncjob import sync_an_people_to_db

def main():
    an = ActionNetworkClient()
    db.Base.metadata.drop_all(db.engine)
    db.Base.metadata.create_all(db.engine)
    sync_an_people_to_db(an, db.Session)


if __name__ == '__main__':
    main()
