

from sqlalchemy import text


views = [
    """
create or replace view member_events_attended as
    select
        member.*,
        action.title as event_title,
        action.start_ts as event_start_ts
    from member
    join attendance on member.action_network_id = attendance.member_action_network_id
    join action on action.action_network_id = attendance.action_action_network_id
    order by action.start_ts desc;
    """,
    """
create or replace view members_in_good_standing as
    select
        member.*
    from member
    join tagging on tagging.member_action_network_id = member.action_network_id
    join tag on tagging.tag_action_network_id = tag.action_network_id
    where tag.name = 'member_in_good_standing';
    """,
]

def create_views(engine):
    with engine.connect() as conn:
        for view in views:
            conn.execute(text(view))
        conn.commit()