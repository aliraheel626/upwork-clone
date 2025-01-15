from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('me/', views.GetCurrentUserData.as_view(), name='user'),
]
