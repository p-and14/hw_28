from django.urls import path, include
from rest_framework import routers

from users import views
from users.views import LocationViewSet

router = routers.SimpleRouter()
router.register("location", LocationViewSet)

urlpatterns = [
    path('user/', views.UserListView.as_view(), name="user_list_view"),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name="user_detail_view"),
    path("user/create/", views.UserCreateView.as_view(), name="user_create"),
    path("user/<int:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("user/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
    path("", include(router.urls), name="location_view_set")
]
