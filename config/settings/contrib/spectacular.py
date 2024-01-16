# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings

SPECTACULAR_SETTINGS = {
    "TITLE": "Project Name API Docs",
    "DESCRIPTION": "Documentation of API endpoints of My Awesome Project",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
}
