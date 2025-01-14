from datetime import datetime
from dataclasses import dataclass
from itertools import chain
import pandas as pd
import streamlit as st
from pymongo import MongoClient

from widgets.data.data_query import instantiate_collection


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


def insert_new_row(new_wine: WineData, client: MongoClient) -> None:
    # convert dataclass to dict
    new_wine_dict = new_wine.__dict__

    # post the new wine to the DB
    collection = instantiate_collection(client)
    collection.insert_one(new_wine_dict)


@st.dialog("Insert your wine")
def insert_wine(data: pd.DataFrame, client: MongoClient) -> None:
    st.write("What wine did you drank?")

    # fields to add new wine
    color = st.radio("Color", ["White", "Rose", "Red", "Fortified"])
    country_col1, country_col2 = st.columns(2)
    with country_col1:
        country = st.selectbox(
            "Country", list(data["country"].unique().tolist()) + ["Other"]
        )
    if country == "Other":
        with country_col2:
            country = st.text_input("Add new country")
    wine_name = st.text_input("Wine Name")
    existent_wine = data[data["wine_name"] == wine_name]
    if wine_name in existent_wine["wine_name"].values:
        st.write("This wine already exists!")
        st.write(existent_wine)
    else:
        if wine_name != "":
            st.write(data[data["wine_name"].str.contains(wine_name)]["wine_name"])

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

                for grape_var in grape_var_addition.split(","):
                    grape_variety.append(grape_var.strip())

    year = st.number_input("Year", 1950, datetime.now().year, value=None)
    price = st.number_input("Price", 15, 1000)
    wine_type = st.selectbox(
        "Type", ["Brut", "Extra-Dry", "Dry", "Semi-Dry", "Semi-Sweet", "Sweet"], index=2
    )
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
