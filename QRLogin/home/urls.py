from django.urls import path

from home.views import home, login_page, logout_page, twofact_setup, add_existing_2fa_code, attempt_login, \
    attempt_2fa_login

app_name = 'home'
urlpatterns = [
    path('login', login_page),
    path('logout', logout_page),
    path('2fa_setup', twofact_setup),
    path('add_existing_2fa_code', add_existing_2fa_code),
    path('attempt_login', attempt_login),
    path('attempt_2fa_login', attempt_2fa_login),

    path('', home),


]