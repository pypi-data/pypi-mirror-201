import pandas as pd
import re

from concurrent.futures import ThreadPoolExecutor
from gandai.datastore import Cloudstore

ds = Cloudstore()


def companies_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/companies")
    if len(keys) == 0:
        return pd.DataFrame(dict(domain=[]))
    table_uris = [f"gs://{ds.BUCKET_NAME}/{k}" for k in keys]
    with ThreadPoolExecutor(max_workers=10) as exec:
        futures = exec.map(pd.read_feather, table_uris)
    df = pd.concat(list(futures))
    df = df.dropna(subset=["domain"])  #
    df = df.drop_duplicates(subset=["domain"])
    return df.reset_index(drop=True)


def events_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/events")
    return pd.DataFrame(ds.load_async(keys))


def comments_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/comments")
    return pd.DataFrame(ds.load_async(keys))


def searches_query() -> pd.DataFrame:
    keys = ds.keys(f"searches/")
    keys = [k for k in keys if k.endswith("search")]
    df = pd.DataFrame(ds.load_async(keys))
    df["status"] = df["meta"].apply(lambda x: f"{x.get('status')}")
    df = df[~df["status"].isin(["Completed Engagement", "Dead Post-Mandate"])]
    df["group"] = df["meta"].apply(lambda x: f"{x.get('status')} - {x.get('stage')}")
    df["research"] = df["meta"].apply(lambda x: x.get("research", ""))
    df = df[["key", "label","status", "group", "research"]].fillna("")
    return df.reset_index(drop=True)


def conflict_query() -> pd.DataFrame:
    """Grabs the dealcloud company id and domain"""
    table_uri = f"gs://{ds.BUCKET_NAME}/sources/dealcloud/company_id_domain.feather"
    df = pd.read_feather(table_uri)
    df = (
        df[["dealcloud_id", "domain", "days_since_contact"]]
        .drop_duplicates(subset=["domain"])
        .reset_index(drop=True)
    )
    assert "domain" in df.columns
    return df

### DealCloud Exports

def dealcloud_engagement_query(fp="data/engagement.xlsx") -> pd.DataFrame:
    # DRAFT
    """
    Read in the DealCloud engagements file and return a dataframe
    """
    df = pd.read_excel(fp)
    df.columns = [col.lower().replace(" ", "_").replace(".", "") for col in df.columns]
    assert('dealcloud_id' in df.columns)
    today = pd.to_datetime("today")
    df["modified_days_ago"] = (today - pd.to_datetime(df["modified_date"])).dt.days
    date_cols = [col for col in df.columns if col.endswith("_date")]

    for col in date_cols:
        df[col] = df[col].apply(lambda x: str(x)[0:10])
    df = df.dropna(subset="engagement_name")  # never hit this condition
    df = df.sort_values("modified_date", ascending=False)
    return df


def dealcloud_company_query(fp="data/company.xlsx") -> pd.DataFrame:
    def _get_domain(url) -> str:
        url = url.replace("http://", "").replace("https://", "").replace("www.", "")
        return url.split("/")[0]

    df = pd.read_excel(fp)  # hmm why so slow, maybe just select specific columns?
    df.columns = [col.replace(" ", "_").replace(".", "").lower() for col in df.columns]
    assert('dealcloud_id' in df.columns)
    df["domain"] = df["website"].dropna().apply(_get_domain)
    df["days_since_contact"] = (
        df["days_since_contact"].dropna().apply(lambda x: int(re.findall(r"\d+", x)[0]))
    )
    df = (
        df[["dealcloud_id","company_name", "domain", "days_since_contact"]]
        .drop_duplicates(subset=["domain"])
        .reset_index(drop=True)
    )
    return df

def dealcloud_target_query(fp = "data/target.xlsx", max_days_in_current_stage=365) -> pd.DataFrame:
    df = pd.read_excel(fp)
    df.columns = [col.replace(" ", "_").replace(".", "").lower() for col in df.columns]
    assert('dealcloud_id' in df.columns)
    df = df[df['days_in_current_stage'] <= max_days_in_current_stage]
    df = df.sort_values("days_in_current_stage").reset_index(drop=True)
    # print(df.columns)
    cols = [
        'engagement','company_name','days_in_current_stage','stage', 'status', 'ga_notes','target_added_date','target_tier'
    ]
    df = df[cols].reset_index(drop=True)
    return df