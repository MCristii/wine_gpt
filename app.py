import streamlit as st
import yaml
from datetime import datetime
import base64

from widgets.authentication.login_widget import authenticator, config
from widgets.authentication.reset_password import reset_password
from widgets.authentication.user_registration import user_registration
from widgets.initialize import initialize_session_status
from widgets.data.insert_wine_data import insert_wine
from widgets.data.filtering import filter_dataframe
from widgets.data.data_query import init_connection, read_mongo_data, process_data
from widgets.data.changes import change_wine_data


initialize_session_status()

st.write(
    """
        # Wine GPT app
    """
)

name, authentication_status, username = authenticator.login(max_login_attempts=10)

if not authentication_status:
    if st.button("Register"):
        user_registration()

if authentication_status:
    with st.sidebar:
        authenticator.logout()
        if st.button("Reset password"):
            reset_password()

    st.write(f"Welcome *{name}*")

    ##################### CONTENT HERE #########################
    client = init_connection()
    data = read_mongo_data()
    data = process_data(data)

    if "Wine inserted" not in st.session_state:
        if st.button("Insert Wine"):
            insert_wine(data, client)

    subheader, filter_wine_toggle = st.columns([3, 1])

    if filter_wine_toggle.toggle("Filter wine data"):
        data = filter_dataframe(data)

    subheader.subheader("Wine data")
    column_config = {
        "price": st.column_config.NumberColumn(
            "price",
            help="The price of the wine in RON",
            min_value=0,
            max_value=1000,
            step=1,
            format="RON %d",
        ),
        "year": st.column_config.NumberColumn(
            "year",
            help="The year of the wine",
            min_value=1950,
            max_value=datetime.now().year,
            step=1,
            format="%d",
        ),
    }
    st.dataframe(data, column_config=column_config)

    if "Wine changed" not in st.session_state:
        if st.button("Change Wine"):
            change_wine_data()

    ############################################################

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

with open("widgets/authentication/auth_config.yaml", "w") as file:
    yaml.dump(config, file, default_flow_style=False)


# background image
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = (
        """
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    """
        % bin_str
    )
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background("./images/wine_background_3.jpg")
