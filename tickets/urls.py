from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tickets'

urlpatterns = [
    path ('ticket_list/',views.tickets ,name= 'ticket_list'),
    path ('ticket_closed_list/',views.show_closed_tickets ,name= 'ticket_closed_list'),
    path("ajax/detail/<int:pk>/", views.ticket_detail_ajax, name="ticket_detail_ajax"),
    path('tickets/<int:pk>/withdrawal_ticket/', views.withdrawal_ticket, name='withdrawal_ticket'),
    path('tickets/<int:id>/add_ticket_message/', views.add_ticket_message, name='add_ticket_message'),
    path('tickets/<int:id>/close/',views.close_ticket , name = 'close_ticket'),
    path ('tickets/new_ticket',views.new_ticket ,name = 'new_ticket'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)