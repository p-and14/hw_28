from django.urls import path

from ads import views

urlpatterns = [
    path("", views.CategoriesListView.as_view(), name="categories_list_view"),
    path("<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail_view"),
    path("create/", views.CategoryCreateView.as_view(), name="category_create_view"),
    path("<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category_update_view"),
    path("<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete_view"),
]
