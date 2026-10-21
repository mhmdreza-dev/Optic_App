from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'education'

urlpatterns = [

    path("education/", views.education_home, name="education_home"),
    path("video/<int:video_id>/", views.education_home, name="video_detail"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)