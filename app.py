import streamlit as st
from datetime import datetime
import yaml
import base64

from widgets.initialize import initialize_session_status
from widgets.authentication.login_widget import authenticator, config
from widgets.authentication import user_registration, reset_password
from widgets.data.insert_wine_data import insert_wine
from widgets.data.filtering import filter_dataframe
from widgets.data.data_query import init_connection, read_mongo_data, process_data
from widgets.data.changes import change_wine_data

# from descope.descope_client import DescopeClient

# DESCOPE_PROJECT_ID = str(st.secrets.get("descope").get("DESCOPE_PROJECT_ID"))
ADMIN_FLAG = 1
# descope_client = DescopeClient(project_id=DESCOPE_PROJECT_ID)

initialize_session_status()

st.write(
    """
        # Wine GPT app
    """
)

name, authentication_status, username = authenticator.login(max_login_attempts=10)
# if "token" not in st.session_state:
#     # User is not logged in
#     if "code" in st.query_params:
#         # Handle possible login
#         code = st.query_params["code"]
#         # Reset URL state
#         st.query_params.clear()
#         try:
#             # Exchange code
#             with st.spinner("Loading..."):
#                 jwt_response = descope_client.sso.exchange_token(code)
#             st.session_state["token"] = jwt_response["sessionToken"].get("jwt")
#             st.session_state["refresh_token"] = jwt_response["refreshSessionToken"].get(
#                 "jwt"
#             )
#             st.session_state["user"] = jwt_response["user"]
#             st.rerun()
#         except Exception as e:
#             st.error(f"Login failed! \n\n{e}")
#     with st.container(border=True):
#         if st.button("Sign In with Google", use_container_width=True):
#             oauth_response = descope_client.oauth.start(
#                 provider="google", return_url="https://winegpt.streamlit.app/"
#             )
#             url = oauth_response["url"]
#             # Redirect to Google
#             st.markdown(
#                 f'<meta http-equiv="refresh" content="0; url={url}">',
#                 unsafe_allow_html=True,
#             )

if not authentication_status:
    if st.button("Register"):
        user_registration()

if authentication_status:
    with st.sidebar:
        authenticator.logout()
        if st.button("Reset password"):
            reset_password()

    st.write(f"Welcome *{name}*")

    # else:
    #     # User is logged in
    #     try:
    #         with st.spinner("Loading..."):
    #             jwt_response = descope_client.validate_and_refresh_session(
    #                 st.session_state.token, st.session_state.refresh_token
    #             )
    #             # Persist refreshed token
    #             st.session_state["token"] = jwt_response["sessionToken"].get("jwt")

    #         user_info_col, logout_col = st.columns([6, 1])

    #         if logout_col.button("Logout"):
    #             # Log out user
    #             del st.session_state.token
    #             st.rerun()

    #         if "user" in st.session_state:
    #             user = st.session_state.user
    #             user_info_col.write("Name: " + user["name"])
    #             user_info_col.write("Email: " + user["email"])

    #         if "Tenant Admin" in user["roleNames"]:
    #             # Show admin-specific content
    #             ADMIN_FLAG = 1

    ##################### CONTENT HERE #########################
    client = init_connection()
    data = read_mongo_data()
    data = process_data(data)

    if ADMIN_FLAG:
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

    if ADMIN_FLAG:
        if "Wine changed" not in st.session_state:
            if st.button("Change Wine"):
                change_wine_data()

    ############################################################

# except Exception:
#     # Log out user
#     del st.session_state.token
#     st.rerun()

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
