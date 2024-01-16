from config.settings.environment import env

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOWED_ORIGINS = env.list("ALLOWED_ORIGINS", default=["http://localhost:3000", "http://localhost:9600"])

ALLOWED_ORIGIN_REGEXES = env.list("CORS_ALLOWED_ORIGIN_REGEXES", default=CORS_ALLOWED_ORIGINS)
