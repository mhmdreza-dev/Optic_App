from django.shortcuts import render ,redirect
from .forms import UserLoginForm ,forms
from .models import User
from tickets.models import Ticket
from django.contrib.auth import authenticate ,login ,logout

# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')

    if request.method == "POST":
        form = UserLoginForm(request.POST) # create An example where the user has entered information
        if form.is_valid():
            data = form.cleaned_data

            try:
                user = authenticate(request ,username = User.objects.get(username = data ['username']
                                                                         ,password = data ['password']))
                
            except:
                user = authenticate(request ,username = data ['username'],password = data ['password'])
            
            if user is not None:
                if user.is_active :

                    login (request,user)
                    #messages.success(request,'با موفقیت وارد شدید.','success')
                    return redirect ('accounts:home')
                else:
                    raise forms.ValidationError ('کاربر غیر فعال است')
            else:

                #messages.success(request,'نام کاربر یا رمز عبور اشتباه است','danger')
                redirect ('accounts:user_login')

    return render(request , 'accounts/login_page.html')  

def home (request):
    user = request.user #کاربر لاگین کرده
    user_tickets = Ticket.objects.filter(creator = request.user)
    total_tickets = user_tickets.count()
    open_tickets = user_tickets.filter(status='open').count() 
    in_progress_tickets = user_tickets.filter(status='progress').count() 
    closed_tickets = user_tickets.filter(status='closed').count()
    context = {
        'employee_code' : user.employee_code ,
        'username' : user.username ,
        'firstname' : user.first_name,
        'lastname': user.last_name,
        'total_tickets':total_tickets ,
        'open_tickets':open_tickets ,
        'in_progress_tickets' : in_progress_tickets ,
        'closed_tickets' : closed_tickets

    }
    return render (request,'accounts/home_page.html' , context)



def user_logout (request):
    logout(request)
    return redirect('accounts:user_login')