"""
solarverse URL Configuration
"""
from django.apps import apps
from django.urls import include, path, re_path
from django.contrib import admin
from django.shortcuts import render
from customapps.enquiry.views import EnquiryView
from customapps.api.views.login import RegistrationCompleteView
from customapps.api.views.otp_view import GenerateOTPView, VerifyOTPView
from customapps.api.views.password_reset import PasswordResetView,PasswordResetConfirmView
# from oscar.views.decorators import *
from customapps.utils.decorators import *

# def render_react(request):
#     return render(request, "index.html")


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    path('admin/', admin.site.urls),
    path('api/', include("oscarapi.urls")),
    path('api/register/complete/',RegistrationCompleteView.as_view(), name='complete_register'),
    path('api/generate-otp/', login_required(GenerateOTPView.as_view()), name='generate_otp'),
    path('api/verify-otp/', login_required(VerifyOTPView.as_view()), name='verify_otp'),
    path('api/password-reset/', login_forbidden(PasswordResetView.as_view()), name='reset_password'),
    path('api/password-reset/confirm/', login_forbidden(PasswordResetConfirmView.as_view()), name='confirm_reset_password'),
    # path('', TemplateView.as_view(template_name="blog/index.html")),
    # path('api/social/', include('allauth.urls')),
    path('api/enquiry/', EnquiryView.as_view(), name="enquiry"),
    # path('accounts/', include('allauth.urls')),
    # path('enquiry/', include("inquirydata.urls")),
    path('api/social/', include('social_django.urls', namespace='social')),
    # path('social-auth/<str:provider>/', social_auth, name='social_auth'),
    # path('social-auth/complete/<str:provider>/', views.social_auth_complete, name='social_auth_complete'),
        # Oscar Bundles API URLs
    # re_path(r"^api/", include(apps.get_app_config("oscarbundles_api").urls[0])),
    # re_path(r"^api/", include("oscarapi.urls")),
    # Oscar Bundles Dashboard URLs
    # re_path(
#         r"^dashboard/", include(apps.get_app_config("oscarbundles_dashboard").urls[0])
#     ),
#     # Include stock Oscar
     re_path(r"^", include(apps.get_app_config("oscar").urls[0])),
# ]

    #JWT
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

#    path('', include(apps.get_app_config('oscar').urls[0])),
    # re_path(r"^$", render_react),
    # re_path(r"^(?:.*)/?$", render_react),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
