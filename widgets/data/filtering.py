from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
)
import pandas as pd
import streamlit as st


def target_grapes(grapes, grapes_to_find):
    return "".join(map(str, grapes_to_find)) in "".join(map(str, grapes))


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    # modify = st.checkbox("Add filters")

    # if not modify:
    #     return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            _, right = st.columns((1, 20))
            # create special usecase for column that contains list as values
            if column == "grape_variety":
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[
                        df["grape_variety"].apply(
                            lambda x: target_grapes(x, user_text_input)
                        )
                    ]

            # Treat columns with < 10 unique values as categorical
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 8:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100

                # apply special condition for 'year' column
                if column == "year":
                    _min, _max, step = int(_min), int(_max), 1

                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]

            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
