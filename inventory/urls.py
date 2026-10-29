from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'inventory'

urlpatterns = [
    path ('transfers_list/',views.transfers_list ,name= 'transfers_list'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)