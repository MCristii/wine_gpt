import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


with open("widgets/authentication/auth_config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)
