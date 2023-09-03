
from django.urls import path
from API.views import RegisterApi, ListUser,LoginApi, ProfileCreateAPI

urlpatterns = [
    path('list/', ListUser.as_view()),
    path('register/', RegisterApi.as_view(), name='register_user'),
    path('login/', LoginApi.as_view(), name='login_user'),
    path('profile/', ProfileCreateAPI.as_view(), name="profile_api"),
    path('profile/<int:pk>/', ProfileCreateAPI.as_view(), name="profile_api")
]


