import streamlit as st
from widgets.authentication.login_widget import authenticator


def reset_password():
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"], location='sidebar'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)
