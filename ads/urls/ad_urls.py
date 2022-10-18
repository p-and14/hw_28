from django.conf.urls.static import static
from django.urls import path

from ads import views
from hw_28 import settings

urlpatterns = [
    path('', views.AdListView.as_view(), name="ads_list_view"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad_detail_view"),
    path("create/", views.AdCreateView.as_view(), name="ad_create_view"),
    path("<int:pk>/update/", views.AdUpdateView.as_view(), name="ad_update_view"),
    path("<int:pk>/delete/", views.AdDeleteView.as_view(), name="ad_delete_view"),
    path("<int:pk>/upload_image/", views.AdImageUploadView.as_view(), name="ad_image_upload_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
