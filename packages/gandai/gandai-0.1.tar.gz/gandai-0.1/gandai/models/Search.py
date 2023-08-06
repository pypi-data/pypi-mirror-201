from time import time
from gandai.datastore import Cloudstore
from gandai.models import Event
from gandai.services import Query

ds = Cloudstore()


def load_search(key: str, actor_key: str = "") -> dict:
    SEARCH_BASE = f"searches/{key}"
    return ds[f"{SEARCH_BASE}/search"]

def load_sort(key: str, actor_key: str = "") -> dict:
    SEARCH_BASE = f"searches/{key}"
    return ds[f"{SEARCH_BASE}/sort"]

def load_filters(key: str, actor_key: str = "") -> dict:
    SEARCH_BASE = f"searches/{key}"
    return ds[f"{SEARCH_BASE}/filters"]


def load_targets(key: str, actor_key: str = "") -> dict:
    def _get_comments(domain: str) -> list:
        if len(comments) == 0:
            return []
        return comments.query("domain == @domain").to_dict(orient="records")

    def _get_events(domain: str) -> list:
        if len(events) == 0:
            return []
        df = events[events["domain"] == domain]
        df = df[df["type"] != "rating"]  # rm fit events
        return df.to_dict(orient="records")

    def _get_rating(domain: str) -> int:
        if len(events) == 0:
            return None
        df = events[events["domain"] == domain]
        df = df[df["type"] == "rating"]
        if len(df) == 0:
            return None
        data = df.to_dict(orient="records")[-1]
        return data["data"]["rating"]

    def _targets_by_state(last_event_type: str, filters: dict={}) -> list:
        """Apply filters on a per state basis"""
        df = targets.query("last_event_type == @last_event_type")
        if len(df) == 0:
            return []
        for k, v in filters.items():
            if k == "employee_range":
                min = v[0]
                if v[1] == 10000:
                    max = 100000000
                else:
                    max = v[1]
                df = df[df['employee_count'] >= min]
                df = df[df['employee_count'] <= max]
            elif k == "ownership":
                df = df[df[k].isin(v["include"])]
                df = df[~df[k].isin(v["exclude"])]
            elif k == "country":
                if len(v) > 0:
                    df = df[df["country"].isin(v)]
            elif k == "state":
                if len(v) > 0:
                    df = df[df["state"].isin(v)]
            print(k, df.shape)

        if "limit" in filters.keys():
            # chopping block
            df = df[0 : filters["limit"]["results"]]

        return df.fillna("").to_dict(orient="records")


    t0 = time()
    companies = Query.companies_query(key)
    t1 = time()
    events = Query.events_query(key)
    t2 = time()
    comments = Query.comments_query(key)
    t3 = time()
    conflicts = Query.conflict_query()
    t4 = time()
    print(f"companies_query: {round(t1-t0, 1)}")
    print(f"events_query: {round(t2-t1, 1)}")
    print(f"comments_query: {round(t3-t2, 1)}")
    print(f"dealcloud_company_query: {round(t4-t3, 1)}")
    print("queries:", (time() - t0))

    companies["comments"] = companies["domain"].apply(_get_comments)
    companies["events"] = companies["domain"].apply(_get_events)
    companies["rating"] = companies["domain"].apply(_get_rating)
    companies["last_event_type"] = companies["events"].apply(
        lambda x: x[-1]["type"] if len(x) > 0 else "created"
    )

    companies = companies.merge(
        conflicts, how="left", left_on="domain", right_on="domain"
    )
    companies["dealcloud_id"] = companies["dealcloud_id"].fillna("")
    
    
    targets = companies
    
    if len(targets) > 0:
        sort = load_sort(key)
        targets = targets.sort_values(
            [sort['sort_field']], 
            ascending=(sort['sort_order'] == "asc")
        )

    filters = load_filters(key)

    resp = {
        "inbox": _targets_by_state("created", filters=filters),
        "review": _targets_by_state("advance", filters=filters),
        "validate": _targets_by_state("validate"),
        "send": _targets_by_state("send"),
        "accept": _targets_by_state("accept"),
        "reject": _targets_by_state("reject"),
        "conflict": _targets_by_state("conflict"),
    }

    return resp
