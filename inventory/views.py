from django.shortcuts import render

# Create your views here.

def transfers_list (request):
    pass

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewTransferForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewTransferForm

@login_required
def new_transfer(request):
    next_url = request.POST.get('next') or request.headers.get('Referer') or 'inventory:transfer_list'

    if request.method == 'POST':
        form = NewTransferForm(request.POST, user=request.user)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.creator = request.user
            transfer.save()
            messages.success(request, 'درخواست انتقالی با موفقیت ثبت شد.')
            return redirect(next_url)
        else:
            # چاپ دقیق خطاها در ترمینال
            print("❌ خطاهای فرم انتقالی:", form.errors)
            
            # استخراج و نمایش خطاها به صورت خوانا برای کاربر
            error_messages = []
            for field, errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields else field
                error_messages.append(f"{field_label}: {', '.join(errors)}")
            
            messages.error(request, 'خطا در ثبت فرم: ' + ' | '.join(error_messages))
            return redirect(next_url)

    else:
        form = NewTransferForm(user=request.user)

    return render(request, 'inventory/transfer_list.html', {'transfer_form': form})

