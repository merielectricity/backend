import os

# Social-Auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
    "https://www.googleapis.com/auth/user.phonenumbers.read",
]

SOCIAL_AUTH_FACEBOOK_KEY=os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET=os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")
#SOCIAL_AUTH_FACEBOOK_SCOPE=["email"]

