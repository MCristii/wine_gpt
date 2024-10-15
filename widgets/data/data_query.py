from pymongo import MongoClient
import pandas as pd
import streamlit as st
from ast import literal_eval


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongodb"]["host"])


# Pull data from the collection.
# You can use st.cache_data to only rerun when the query changes or after 10 min.
def get_data() -> list:
    client = init_connection()
    db = client[st.secrets["mongodb"]["database"]]
    items = db[st.secrets["mongodb"]["collection"]].find()
    items = list(items)  # make hashable for st.cache_data
    return items


def read_mongo_data(no_id=True) -> pd.DataFrame:
    """Read from Mongo and Store into DataFrame"""
    items = get_data()

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(items)

    # Delete the _id
    if no_id:
        del df["_id"]

    return df


def lowercase(x):
    return str(x).lower()


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    data["grape_variety"] = (
        data["grape_variety"].astype(str).apply(lambda x: literal_eval(x))
    )
    data.rename(lowercase, axis="columns", inplace=True)
    return data


def instantiate_collection(client: MongoClient):
    secrets = st.secrets["mongodb"]
    collection = client[secrets["database"]][secrets["collection"]]
    return collection
