"""
solarverse URL Configuration
"""
from django.apps import apps
from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static
from django.shortcuts import render
from customapps.enquiry.views import EnquiryView
from customapps.api.views.login import RegistrationCompleteView
from customapps.api.views.otp_view import GenerateOTPView, VerifyOTPView
from customapps.api.views.password_reset import PasswordResetView,PasswordResetConfirmView
from customapps.utils.decorators import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from django.shortcuts import render

def render_react(request):
    return render(request, 'index.html')


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    path('admin/', admin.site.urls),
    path('api/', include("oscarapi.urls")),
    path('api/register/complete/',RegistrationCompleteView.as_view(), name='complete_register'),
    path('api/generate-otp/', GenerateOTPView.as_view(), name='generate_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('api/password-reset/', PasswordResetView.as_view(), name='reset_password'),
    path('api/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='confirm_reset_password'),
    path('api/enquiry/', EnquiryView.as_view(), name="enquiry"),
    path('api/social/', include('social_django.urls', namespace='social')),
    # re_path(r"^", include(apps.get_app_config("oscar").urls[0])),
    #JWT
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react),
    # path('', ReactAppView.as_view(), name='react-app'),
    # re_path(r'^static/(?P<path>.*)', serve_static),
    # path('', react_index, name='index'), 
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
