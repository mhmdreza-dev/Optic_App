
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect ,render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Ticket
from accounts.models import User
from .forms import TicketMessageForm
from django.http import JsonResponse
from .forms import NewTicketForm ,TicketMessageForm
from .models import TicketAttachment ,Ticket 
from django.db.models import Max
from django.shortcuts import get_object_or_404
# Create your views here.

# تابع فهرست تیکت ها
def tickets(request):

    #اگر کاربر پشتیبان بود
    if request.user.is_staff:

        tickets = Ticket.objects.filter(
            destination_unit=request.user.unit).exclude(status='closed').prefetch_related("attachments", "messages").order_by('-id')

    
        paginator = Paginator(tickets, 15)  # هر صفحه 7 تیکت

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'tickets': page_obj
        }
    #اگر کاربر پشتیبان نبود
    if not request.user.is_staff:

        tickets = Ticket.objects.filter(
            creator = request.user).exclude(status='closed').prefetch_related("attachments", "messages").order_by('-id')

        paginator = Paginator(tickets, 7)  # هر صفحه 7 تیکت

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'tickets': page_obj ,

        }


    return render(request, 'tickets/tickets_list.html', context)

# تابع فهرست تیکت های بسته شده
def show_closed_tickets(request):

        
    tickets = Ticket.objects.filter(status='closed',destination_unit = request.user.unit).prefetch_related("attachments", "messages").order_by('-id')

    paginator = Paginator(tickets, 7)  # هر صفحه 7 تیکت

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
            'tickets': page_obj
        }

    return render(request, 'tickets/tickets_list.html', context)

# تابع نمایش جزئیات تیکت ها
def ticket_detail_ajax(request, pk):
    ticket = get_object_or_404(
        Ticket.objects.select_related("creator"),
        pk=pk
    )
    colleagues = User.objects.filter(
                                    unit=request.user.unit,
                                    is_staff=True,
                                    is_active=True
                                    ).exclude(id=request.user.id)
    return render(
        request,
        "tickets/ticket_detail_content.html",
        {"ticket": ticket ,
         'unit_colleagues': colleagues
        }
    )

#تابع برداشتن تیکت
@require_POST  # برای امنیت بیشتر فقط متد POST را قبول می‌کنیم
def withdrawal_ticket (request,pk):
    
    ticket = get_object_or_404(Ticket, id = pk)
    ticket.status = 'progress'
    ticket.taken_by = request.user
    ticket.taken_time = timezone.now()
    ticket.save()
    
    return JsonResponse({'status': 'success', 'message': 'تیکت با موفقیت برداشته شد.'})



@login_required
def add_ticket_message(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    print (request.user != ticket.creator , not request.user.is_staff)
    if ( not request.user.is_staff ) and ( request.user != ticket.creator )  :
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'شما دسترسی ندارید.'}, status=403)
        return HttpResponseForbidden("شما دسترسی به این تیکت ندارید.")
    
    if request.method == "POST":
        form = TicketMessageForm(request.POST)
        
        if form.is_valid():
            message_obj = form.save(commit=False)
            message_obj.ticket = ticket
            message_obj.sender = request.user
            if request.user.is_staff:
                message_obj.is_staff_reply = True
            message_obj.save()
            
            # ✅ برای درخواست‌های AJAX، JSON برگردون
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'پیام با موفقیت ارسال شد.'
                })
            
            # برای درخواست‌های معمولی، redirect کن
            messages.success(request, "پیام شما با موفقیت ارسال شد.")
            return redirect('tickets:ticket_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'لطفاً فرم را به درستی پر کنید.'
                }, status=400)
    
    return redirect('tickets:ticket_list')


@login_required
def close_ticket (request , id):
    if request.method == 'POST':
        ticket = get_object_or_404(Ticket, id=id)
        ticket.status = 'closed'
        ticket.expiration_time = timezone.now()
        ticket.save()
        return JsonResponse({'status': 'success', 'message': 'تیکت با موفقیت بسته شد'})


# تابع ایجاد تیکت جدید
def new_ticket (request):

    if request.method == "POST":
        
        form = NewTicketForm(request.POST)

        if form.is_valid():

            ticket = form.save(commit = False)
            ticket.creator = request.user
            max_num = Ticket.objects.aggregate(Max('ticket_number'))['ticket_number__max']
            ticket.ticket_number = (int (max_num) or 0) + 1
            ticket.save()
            # دریافت فایل‌های ارسالی از اینپوت با نام 'files'
            files = request.FILES.getlist('files')
            # حلقه زدن و ساخت آبجکت برای هر فایل
            for f in files:
                TicketAttachment.objects.create(
                    ticket=ticket, 
                    file=f
                )
            messages.success(request, "تیکت شما با موفقیت ثبت شد.")
            return redirect(request.META.get('HTTP_REFERER', 'tickets:list')) # یا هر جایی که می‌خواهی برگردد
        
    else:
        form = NewTicketForm()
    
        # فحه‌ای که مودال توش قرار داره رو رندر کن (مثلاً ticket_list.html)
        return render(request, 'tickets/ticket_list.html', {'ticket_form': form})


# تابع ارجاع تیکت جدید
def reassign_ticket(request , ticket_id ,colleagues_id):

    ticket = get_object_or_404(Ticket, id = ticket_id)
    ticket.reference_to = User.objects.get(id=colleagues_id)
    ticket.save()
    messages.success(request, "پیام شما با موفقیت ارجاع شد.")
    return redirect('tickets:ticket_list')


# تابع نمایش تیک های ارجاع شده 
def referenced_ticket (request):


    #اگر کاربر پشتیبان بود
    if request.user.is_staff:

        tickets = Ticket.objects.filter(
            destination_unit=request.user.unit , reference_to = request.user.id).exclude(status='closed').prefetch_related("attachments", "messages").order_by('-id')

    
        paginator = Paginator(tickets, 15)  # هر صفحه 7 تیکت

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'tickets': page_obj
        }
    #اگر کاربر پشتیبان نبود
    if not request.user.is_staff:

        tickets = Ticket.objects.filter(
            reference_to = request.user).exclude(status='closed').prefetch_related("attachments", "messages").order_by('-id')

        paginator = Paginator(tickets, 7)  # هر صفحه 7 تیکت

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'tickets': page_obj ,

        }


    return render(request, 'tickets/referenced_tickets_list.html', context)