import os

from .utils import get_setting

AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "")

GRAPH_CLIENT_ID = os.environ.get("GRAPH_CLIENT_ID", AZURE_CLIENT_ID)
GRAPH_CLIENT_SECRET = os.environ.get("GRAPH_CLIENT_SECRET", AZURE_CLIENT_SECRET)

AZURE_SSL = True
AZURE_URL_EXPIRATION_SECS = 10800
AZURE_ACCESS_POLICY_EXPIRY = 10800  # length of time before signature expires in seconds
AZURE_ACCESS_POLICY_PERMISSION = "r"
AZURE_TOKEN_URL = "https://login.microsoftonline.com/unicef.org/oauth2/token"
AZURE_GRAPH_API_BASE_URL = "https://graph.microsoft.com"
AZURE_GRAPH_API_VERSION = os.environ.get("AZURE_GRAPH_API_VERSION", "v1.0")  # beta
AZURE_GRAPH_API_PAGE_SIZE = 300

AZURE_LOGOUT_BASE_URL = get_setting(
    ["SOCIAL_AUTH_TENANT_B2C_URL", "TENANT_B2C_URL", "AZURE_LOGOUT_BASE_URL"],
    default="login.microsoftonline.com",
)
AZURE_POLICY = get_setting(["SOCIAL_AUTH_POLICY", "TENANT_POLICY"])
AZURE_TENANT_ID = get_setting(["SOCIAL_AUTH_TENANT_ID", "TENANT_ID"])
AZURE_RESET_POLICY = get_setting(
    ["SOCIAL_AUTH_PASSWORD_RESET_POLICY", "PASSWORD_RESET_POLICY"]
)

UNICEF_EMAIL = os.environ.get("UNICEF_EMAIL", "@unicef.org")
