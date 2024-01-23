from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# API URLS
api_urlpatterns = [
    path("auth/", include("klm.users.api.urls")),
    path("", include("klm.intelligence.urls"))
]

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
    path("api/", include(api_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs",),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),

]
# if settings.DEBUG:
#     # This allows the error pages to be debugged during development, just visit
#     # these url in browser to see how these error pages look like.
#     if "debug_toolbar" in settings.INSTALLED_APPS:
#         import debug_toolbar
#
#         urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
