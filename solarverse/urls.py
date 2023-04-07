"""
solarverse URL Configuration
"""
from django.apps import apps
from django.urls import include, path, re_path
from django.contrib import admin
from django.shortcuts import render

def render_react(request):
    return render(request, "index.html")


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    path('admin/', admin.site.urls),
    path("api/", include("oscarapi.urls")),
    # path('enquiry/', include("inquirydata.urls")),
    # path('', include("social.apps.django_app.urls",namespace="social")),
    path('', include("social_django.urls"), name='social'),
        # Oscar Bundles API URLs
    # re_path(r"^api/", include(apps.get_app_config("oscarbundles_api").urls[0])),
    # re_path(r"^api/", include("oscarapi.urls")),
    # Oscar Bundles Dashboard URLs
    # re_path(
#         r"^dashboard/", include(apps.get_app_config("oscarbundles_dashboard").urls[0])
#     ),
#     # Include stock Oscar
#     re_path(r"^", include(apps.get_app_config("oscar").urls[0])),
# ]

    path('', include(apps.get_app_config('oscar').urls[0])),
    # re_path(r"^$", render_react),
    # re_path(r"^(?:.*)/?$", render_react),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
