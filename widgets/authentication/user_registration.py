import yaml
import streamlit as st
from widgets.authentication.login_widget import authenticator

def user_registration():
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)
