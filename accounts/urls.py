from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts' 

urlpatterns = [
    path ('',views.user_login ,name= 'user_login'),
    path ('home/',views.home ,name= 'home'),
    path ('logout/',views.user_logout , name = 'user_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)