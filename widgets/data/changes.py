from bson.objectid import ObjectId
import streamlit as st
from widgets.data.data_query import (
    init_connection,
    read_mongo_data,
    instantiate_collection,
    process_data,
)
from widgets.data.filtering import filter_dataframe


def rewrite_wine_data(old_dict, dict_to_update):
    client = init_connection()
    collection = instantiate_collection(client)

    # find the wine to update
    id_filter = {"_id": ObjectId(dict_to_update["_id"])}
    # update all fields
    for (old_key, old_value), (new_key, new_value) in zip(
        old_dict.items(), dict_to_update.items()
    ):
        if old_value != new_value and new_key != "_id":
            st.session_state["newvalues"]["$set"] = {new_key: new_value}

    # save the updates
    collection.update_one(id_filter, st.session_state["newvalues"])


@st.experimental_dialog("Change wine data")
def change_wine_data():
    data = read_mongo_data(no_id=False)

    data = process_data(data)

    data = filter_dataframe(data)
    if data.shape[0] > 1:
        st.write("Filter the data to just 1 wine entry!")
        st.dataframe(data)
    else:
        new_data = st.data_editor(data)
        st.session_state["new_data"] = new_data
        st.session_state["newvalues"] = {}

        if st.toggle("Change grape types"):
            st.write("Current grapes: ")
            st.write(data["grape_variety"])
            grape_varieties = []
            grape_var_addition = st.text_input(
                "Update grape varieties (delimit them by comma)"
            )
            for grape_var in grape_var_addition.split(","):
                grape_varieties.append(grape_var.strip())
            new_data.loc[:, "grape_variety"] = str(grape_varieties)
            st.session_state["new_data"] = new_data

        if st.button("Change wine data"):

            for (_, old_row), (_, new_row) in zip(data.iterrows(), new_data.iterrows()):
                rewrite_wine_data(old_row.to_dict(), new_row.to_dict())

            st.session_state.change_wine_data = {"Wine changed": True}
            st.rerun()
