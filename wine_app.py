
import streamlit as st
import yaml

from widgets.authentication.login_widget import authenticator, config
from widgets.authentication.reset_password import reset_password
from widgets.authentication.user_registration import user_registration
from widgets.initialize import initialize_session_status 
from widgets.data import insert_wine, load_data 


        

initialize_session_status()

st.write(
    """
        # Wine GPT app         
    """
)
if st.button("Register"):
    user_registration()

name, authentication_status, username = authenticator.login(max_login_attempts=10)
    
if authentication_status:
    with st.sidebar:
        authenticator.logout()
        if st.button("Reset password"):
            reset_password()
        
    st.write(f'Welcome *{name}*')

    ##################### CONTENT HERE #########################
    data = load_data()

    if "Wine inserted" not in st.session_state:
        if st.button('Insert Wine'):
            insert_wine(data)
            

    if st.checkbox('Show wine data'):
        st.subheader('Wine data')
        st.dataframe(data)
    ############################################################
    
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
    
with open('widgets/authentication/auth_config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)