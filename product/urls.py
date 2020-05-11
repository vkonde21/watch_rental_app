from django.urls import path
from loginsystem import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from product.views import homepage, productview, checkout, search

urlpatterns = [
    path('home', homepage, name="homepage"),
    path('product/productview/<int:id>', productview, name="productview"),
    path("checkout", checkout, name = " checkout"),
    path("search", search, name="search"),
]


if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL,
                          #document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
