"""
    This file contains the helper code to handle the
    Dash App authentication.

    Currently supports the local Credentials file usage.
"""
import os
import toml

#####################################################
# Credentials SETUP
# This setup should change for deployed application.
# If deployed inside GCP, then authentication is transparent for client libs.
#####################################################
# CREDENTIALS SETUP
script_path = os.path.realpath(__file__)
root_path = os.path.dirname(script_path)
common_path = os.path.join(os.path.dirname(root_path), "common")
CREDENTIALS_PATH = os.path.join(
    os.path.join(common_path, "credentials"), "pub_sub_to_bigquery_credentials.json"
)


####################################################
# GCP values to perform identity platform authentication
####################################################
GCP_FIREBASE_FILE = f"{root_path}/auth.toml"
with open(GCP_FIREBASE_FILE, "r") as f:
    AUTH_CONFIG = toml.load(f)

CLIENT_OAUTH_SECRET = AUTH_CONFIG["oauth_secrets"]
FIREBASE_API_KEY = AUTH_CONFIG["firebase_api_key"]
GOOGLE_OAUTH_REDIRECT = AUTH_CONFIG["oauth_redirect_url"]
FIREBASE_DEFAULT_SERVICE_ACCOUNT = AUTH_CONFIG[
    "firebase_default_service_account"
]
