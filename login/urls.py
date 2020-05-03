
from django.urls import path
from login.views import register,basic,profile
from loginsystem import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', basic,name = "basic"),
    path('register/', register, name = "register"),
    path('login/', auth_views.LoginView.as_view(template_name = 'login/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'login/logout.html'), name="logout"),
    path('profile/',profile, name ='profile')
]


if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL,
                          #document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
