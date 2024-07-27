import streamlit as st
import yaml
from datetime import datetime

from widgets.authentication.login_widget import authenticator, config
from widgets.authentication.reset_password import reset_password
from widgets.authentication.user_registration import user_registration
from widgets.initialize import initialize_session_status
from widgets.data.data import insert_wine, load_data
from widgets.data.filtering import filter_dataframe


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
    data = load_data()

    if "Wine inserted" not in st.session_state:
        if st.button("Insert Wine"):
            insert_wine(data)

    if st.checkbox("Show wine data"):
        if st.toggle("Filter wine data"):
            data = filter_dataframe(data)

        st.subheader("Wine data")
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
    ############################################################

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

with open("widgets/authentication/auth_config.yaml", "w") as file:
    yaml.dump(config, file, default_flow_style=False)
