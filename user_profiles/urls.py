from django.urls import path
from user_profiles.views import (
    RegistrationView,
    # ActivateView,
    # activateConfirm,
    accountActivateView,
    GetCSRFToken, LoginView, LogoutView,
    testSessionView
)
urlpatterns = [
    path('auth/registration/', RegistrationView.as_view(), name='register'),
    path('auth/activate/', accountActivateView.as_view(), name='activate'),
    # path('auth/activate/', activateConfirm.as_view(), name='activate-confirm'),
    path('auth/csrf_cookie/', GetCSRFToken.as_view(), name='csrf_cookie'),
    path('auth/signin/', LoginView.as_view(), name='signin'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('generate/', testSessionView.as_view(), name='generate')
]