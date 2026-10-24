from .forms import NewTicketForm
from .models import Ticket

def global_ticket_form(request):
    return {
        'ticket_form': NewTicketForm()
    }

def ticket_stats_processor(request):
    # مقدار پیش‌فرض صفر
    opened_tickets_count = 0

    # بررسی اینکه کاربر لاگین کرده و پرسنل است و واحد دارد
    if request.user.is_authenticated and request.user.is_staff:
        # اگر در مدل یوزر فیلد unit دارید
        user_unit = getattr(request.user, 'unit', None)
        
        if user_unit:
            opened_tickets_count = Ticket.objects.filter(
                destination_unit=user_unit ,status='open'
            ).count()

    return {
        'opened_tickets_count': opened_tickets_count
    }