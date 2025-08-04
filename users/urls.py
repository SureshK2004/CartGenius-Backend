from django.urls import path
from .views import (
    RegisterUserView,
    VerifyUserEmail,
    LoginUserView,
    TestAuthenticationView,
    PasswordResetRequestView,
    PasswordRestConfirm,
    SetNewPassword,
    LogoutUserView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterUserView.as_view(), name='signup'),
    path('verify-email/', csrf_exempt(VerifyUserEmail.as_view()), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),  
    path('password-reset/', PasswordResetRequestView.as_view(), name="password-reset"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordRestConfirm.as_view(), name="password_reset_confirm"),
    path('set-new-password/', SetNewPassword.as_view(), name='set-new-password'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
