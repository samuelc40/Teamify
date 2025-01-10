from django.urls import path
from userauths.views import *

app_name = 'userauths'

urlpatterns = [
    path("sign-up", register, name='sign-up'),
    path("sign-in", login_view, name='sign-in'),
    path("logout", logout_view, name='logout'),
    path('verify-email/<str:username>/', verify_email, name='verify-email'),
    path('resend-otp/', resend_otp, name='resend-otp'),
    # path('activate-user/<uidb64>/<token>', activate_user, name='activate'),
    # path('signup/', register, name='signup'),
    # path('signin/', login, name='signin'),
]