import pymongo
import pandas as pd
import streamlit as st


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongodb"]["host"])


# Pull data from the collection.
# You can use st.cache_data to only rerun when the query changes or after 10 min.
def get_data(client: pymongo.MongoClient) -> list:
    db = client[st.secrets["mongodb"]["database"]]
    items = db[st.secrets["mongodb"]["collection"]].find()
    items = list(items)  # make hashable for st.cache_data
    return items


def read_mongo_data(client: pymongo.MongoClient, no_id=True) -> pd.DataFrame:
    """Read from Mongo and Store into DataFrame"""

    items = get_data(client)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(items)

    # Delete the _id
    if no_id:
        del df["_id"]

    return df
