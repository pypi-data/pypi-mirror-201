from dataclasses import asdict, dataclass, field
from enum import Enum
from time import time
from typing import Optional

from gandai.datastore import Cloudstore
from gandai.services import Query
from gandai.adapters.grata import GrataWrapper

gw = GrataWrapper()
ds = Cloudstore()


class EventType(str, Enum):
    CREATE = "create"
    ADVANCE = "advance"
    QUALIFY = "qualify"
    REJECT = "reject"
    # FoobarEnum


@dataclass
class Event:
    key: str = field(init=False)
    search_key: str
    domain: str  # fk
    actor_key: str  #
    type: str  # build, advance, qualify, reject, conflict, rate
    data: dict = field(default_factory=dict)
    created: int = field(init=False)

    def __post_init__(self):
        # build, advance, qualify, reject, conflict
        self.created = int(time())
        self.key = f"searches/{self.search_key}/events/{self.created}"


def post_event(
    actor_key: str, search_key: str, domain: str, type: str, data: dict
) -> None:
    event = Event(
        actor_key=actor_key, search_key=search_key, domain=domain, type=type, data=data
    )
    ds[event.key] = asdict(event)
    if type == "advance":
        gw.build_similiar_targets_from_id(
            id=data["id"], search_key=search_key, k=25
        )
    elif type == "validate":
        gw.build_similiar_targets_from_id(
            id=data["id"], search_key=search_key, k=100
        )
    elif type == "accept":
        gw.build_similiar_targets_from_id(
            id=data["id"], search_key=search_key, k=200
        )
    elif type == "conflict":
        # tbd on k, may want to be higher
        gw.build_similiar_targets_from_id(
            id=data["id"], search_key=search_key, k=25
        )
    return f"posted: {event.key}"


def undo_event(key: str, actor_key: str) -> None:
    event = ds[key]
    assert actor_key == event["actor_key"]
    ds.delete(key)  # todo as __del__ or whatever
    return f"deleted: {key}"


def undo_last_event_by_domain(search_key: str, domain: str, actor_key: str) -> None:
    """Only want to be able to undo 'my' events"""
    events = Query.events_query(search_key=search_key)
    events = events[events["actor_key"] == actor_key]
    events = events[events["domain"] == domain]
    events = events.sort_values("created", ascending=False).reset_index(drop=True)
    msg = undo_event(key=events["key"][0], actor_key=actor_key)
    return msg
