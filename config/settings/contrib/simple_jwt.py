from datetime import timedelta

from config.settings.environment import env

SIMPLE_JWT = {
    "USER_ID_FIELD": "uuid",
    "AUTH_HEADER_TYPES": env.tuple(
        "API_SIMPLEJWT_AUTH_HEADER_TYPES",
        default=("Bearer",),
    ),
    "UPDATE_LAST_LOGIN": True,
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env.int("API_SIMPLEJWT_ACCESS_TOKEN_LIFETIME_IN_MINUTES", default=60 * 24)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.float("API_SIMPLEJWT_REFRESH_TOKEN_LIFETIME_IN_DAYS", default=30)),
}
