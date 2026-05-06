
from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
]