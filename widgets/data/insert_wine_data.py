from datetime import datetime
from dataclasses import dataclass
from itertools import chain
import pandas as pd
from ast import literal_eval
import streamlit as st
from pymongo import MongoClient

DATA_PATH = "wine_data.csv"


@dataclass
class WineData:
    color: str
    country: str
    wine_name: str
    grape_variety: list[str]
    year: str
    price: float
    type: str
    sparkling: bool


def lowercase(x):
    return str(x).lower()


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    data["grape_variety"] = (
        data["grape_variety"].astype(str).apply(lambda x: literal_eval(x))
    )
    data.rename(lowercase, axis="columns", inplace=True)
    return data


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data = process_data(data)
    return data


def insert_new_row(new_wine: WineData, client: MongoClient) -> None:
    # convert dataclass to dict
    new_wine_dict = new_wine.__dict__

    # post the new wine to the DB
    secrets = st.secrets["mongodb"]
    collection = client[secrets["database"]][secrets["collection"]]
    collection.insert_one(new_wine_dict)

    # add the new row to the dataframe
    # data.loc[len(data)] = new_wine_dict
    # save the csv
    # data.to_csv("wine_data.csv", index=False)


@st.experimental_dialog("Insert your wine")
def insert_wine(data: pd.DataFrame, client: MongoClient) -> None:
    st.write("What wine did you drank?")

    # fields to add new wine
    color = st.radio("Color", ["White", "Rose", "Red"])
    country_col1, country_col2 = st.columns(2)
    with country_col1:
        country = st.selectbox(
            "Country", list(data["country"].unique().tolist()) + ["Other"]
        )
    if country == "Other":
        with country_col2:
            country = st.text_input("Add new country")
    wine_name = st.text_input("Wine Name")

    grape_var_col1, grape_var_col2 = st.columns(2)
    with grape_var_col1:
        grape_variety = st.multiselect(
            "Grape Variety",
            set([*chain.from_iterable(data["grape_variety"])]).union(["Other"]),
        )
    if "Other" in grape_variety:
        with grape_var_col2:
            grape_var_addition = st.text_input(
                "Add new grape varieties (delimit them by comma)"
            )
            if "Other" in grape_variety:
                grape_variety.remove("Other")
                grape_variety.append(grape_var_addition)

    year = st.number_input("Year", 1950, datetime.now().year, value=None)
    price = st.number_input("Price", 15, 1000)
    wine_type = st.selectbox(
        "Type", ["Brut", "Extra-Dry", "Dry", "Semi-Dry", "Semi-Sweet", "Sweet"]
    )
    st.write(wine_type)
    sparkling = st.toggle("Sparkling")

    # create a WineData dataclass object
    new_wine = WineData(
        color=color,
        country=country,
        wine_name=wine_name,
        grape_variety=grape_variety,
        year=str(year),
        price=price,
        type=wine_type,
        sparkling=sparkling,
    )

    if st.button("Add wine"):
        data = insert_new_row(new_wine, client)
        st.session_state.insert_wine = {"Wine inserted": True}
        st.rerun()
