from django import forms
from .models import Ticket ,TicketMessage


#---------------------------
#   فرم ایجاد تیکت جدید   |
#---------------------------

class NewTicketForm (forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['ticket_title', 'destination_unit', 'priority', 'description']
        widgets = {
            'ticket_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان تیکت را وارد کنید...'}),
            'destination_unit': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    

#---------------------------
#    فرم پاسخ تیکت ها     |
#---------------------------
class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['content']  # فقط content، reply_to حذف شد
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'پیام خود را اینجا بنویسید...', 
                'rows': 3,
                'required': True
            }),
        }
