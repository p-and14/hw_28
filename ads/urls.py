from django.conf.urls.static import static
from django.urls import path

from ads import views
from hw_28 import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('ad/', views.AdListView.as_view(), name="ads_list_view"),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name="ad_detail_view"),
    path("ad/create/", views.AdCreateView.as_view(), name="ad_create_view"),
    path("ad/<int:pk>/update/", views.AdUpdateView.as_view(), name="ad_update_view"),
    path("ad/<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad_delete_view"),
    path("ad/<int:pk>/upload_image/", views.AdImageUploadView.as_view(), name="ad_image_upload_view"),
    path("cat/", views.CategoriesListView.as_view(), name="categories_list_view"),
    path("cat/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail_view"),
    path("cat/create/", views.CategoryCreateView.as_view(), name="category_create_view"),
    path("cat/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category_update_view"),
    path("cat/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
