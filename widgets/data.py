from datetime import datetime
from dataclasses import dataclass
from itertools import chain
import pandas as pd
from ast import literal_eval
import streamlit as st

DATA_PATH = "wine_data.csv"


@dataclass
class WineData:
    color: str
    country: str
    wine_name: str
    grape_variety: list[str]
    year: str
    price: float
    wine_type: str
    sparkling: bool


def lowercase(x):
    return str(x).lower()


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    data["grape_variety"] = data["grape_variety"].apply(lambda x: literal_eval(x))
    data["year"] = data["year"].astype("string")
    data.rename(lowercase, axis="columns", inplace=True)
    return data


def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH, dtype={"year": str})
    data = process_data(data)
    return data


def insert_new_row(new_wine: WineData, data: pd.DataFrame) -> None:
    # convert dataclass to dict
    new_wine_dict = new_wine.__dict__
    # add the new row to the dataframe
    data.loc[len(data)] = new_wine_dict
    # save the csv
    data.to_csv("wine_data.csv", index=False)


@st.experimental_dialog("Insert your wine")
def insert_wine(data: pd.DataFrame) -> None:
    st.write("What wine did you drank?")

    # fields to add new wine
    color = st.radio("Color", ["White", "Rose", "Red"])
    country = st.selectbox("Country", data["country"].unique())
    wine_name = st.text_input("Wine Name")
    grape_variety = st.multiselect(
        "Grape Variety", set([*chain.from_iterable(data["grape_variety"])])
    )
    year = st.number_input("Year", 1950, datetime.now().year)
    price = st.slider("Price", 15, 1000)
    wine_type = st.selectbox(
        "Type", ["Brut", "Extra-Dry", "Dry", "Semi-Dry", "Semi-Sweet", "Sweet"]
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
        wine_type=wine_type,
        sparkling=sparkling,
    )

    st.write(new_wine.__dict__)

    if st.button("Add wine"):
        data = insert_new_row(new_wine, data)
        st.session_state.insert_wine = {"Wine inserted": True}
        st.rerun()
