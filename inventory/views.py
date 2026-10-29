from django.shortcuts import render

# Create your views here.

def transfers_list (request):
    pass

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NewTransferForm

@login_required
def new_transfer(request):
    if request.method == 'POST':
        form = NewTransferForm(request.POST, user=request.user)
        next_url = request.POST.get('next') or request.headers.get('Referer') or 'inventory:transfer_list'
        if form.is_valid():
            transfer = form.save(commit=False)
            
            transfer.creator = request.user
            transfer.save()
            messages.success(request, 'درخواست انتقالی با موفقیت ثبت شد.')
            return redirect(next_url)

        else:
            print("❌ خطاهای فرم انتقالی:", form.errors)
            messages.error(request, 'لطفاً خطاهای فرم را برطرف نمایید.')
            return redirect(next_url)

    else:
        form = NewTransferForm(user=request.user)

    return render(request, 'inventory/transfer_list.html', {'transfer_form': form})
