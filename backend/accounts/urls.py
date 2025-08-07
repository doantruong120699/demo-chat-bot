from django.urls import path
from accounts.views.login import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenLogoutView,
)
from accounts.views.sign_up import SignUpView, VerifyEmailView
from accounts.views.user import UpdateUserView, UserView
from accounts.views.social_sign_up import auth_google_callback
from accounts.views.user import ChangePasswordView


urlpatterns = [
    path("auth/login", CustomTokenObtainPairView.as_view(), name="login"),
    path("auth/logout", CustomTokenLogoutView.as_view(), name="logout"),
    path("auth/token/refresh", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/sign-up", SignUpView.as_view(), name="sign_up"),
    path("auth/verify-email", VerifyEmailView.as_view(), name="verify_email"),
    path("account/me", UserView.as_view(), name="get_me"),
    # Social
    path(
        "auth/google/callback",
        view=auth_google_callback,
        name="auth_google_callback",
    ),
    path(
        "account/change-password", ChangePasswordView.as_view(), name="change_password"
    ),
    path("account/update", UpdateUserView.as_view(), name="update_user"),
]
