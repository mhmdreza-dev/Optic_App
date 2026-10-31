from .forms import NewTransferForm
from .models import Transfers

def global_transfer_form(request):
    return {
        'transfer_form': NewTransferForm()
    }


def transfer_modal_context(request):
    """
    این تابع فرم انتقالی را همراه با یوزر فعال در دسترس تمام صفحات قرار می‌دهد
    """
    if request.user.is_authenticated:
        return {
            'global_transfer_form': NewTransferForm(user=request.user)
        }
    return {
        'global_transfer_form': None
    }


# def ticket_stats_processor(request):
#     # مقدار پیش‌فرض صفر
#     opened_tickets_count = 0

#     # بررسی اینکه کاربر لاگین کرده و پرسنل است و واحد دارد
#     if request.user.is_authenticated and request.user.is_staff:
#         # اگر در مدل یوزر فیلد unit دارید
#         user_unit = getattr(request.user, 'unit', None)
        
#         if user_unit:
#             opened_tickets_count = Ticket.objects.filter(
#                 destination_unit=user_unit ,status='open'
#             ).count()

#     return {
#         'opened_tickets_count': opened_tickets_count
#     }

# def ticket_referenced (request):
#     # مقدار پیش‌فرض صفر
#     referenced_tickets_count = 0

#     # بررسی اینکه کاربر لاگین کرده و پرسنل است و واحد دارد
#     if request.user.is_authenticated and request.user.is_staff:
#         # اگر در مدل یوزر فیلد unit دارید
#         user_unit = getattr(request.user, 'unit', None)
        
#         if user_unit:
#             referenced_tickets_count = Ticket.objects.filter(
#                 reference_to = request.user
#             ).exclude(status='closed').count()

#     return {
#         'referenced_tickets_count': referenced_tickets_count
#     }