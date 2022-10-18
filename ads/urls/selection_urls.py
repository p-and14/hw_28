from django.urls import path

from ads import views

urlpatterns = [
    path("", views.SelectionListView.as_view(), name="selection_list_view"),
    path("<int:pk>/", views.SelectionDetailView.as_view(), name="selection_detail_view"),
    path("create/", views.SelectionCreateView.as_view(), name="selection_create_view"),
    path("<int:pk>/update/", views.SelectionUpdateView.as_view(), name="selection_update_view"),
    path("<int:pk>/delete/", views.SelectionDeleteView.as_view(), name="selection_delete_view"),
]
