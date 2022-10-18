from django.conf.urls.static import static
from django.urls import path, include

from ads import views
from hw_28 import settings

urlpatterns = [

    path('ad/', include("urls.ad_urls")),
    path('cat/', include("urls.category_urls")),
]


