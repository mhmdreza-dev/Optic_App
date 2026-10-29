from django import forms
from .models import Transfers
from accounts.models import Store, Unit

class NewTransferForm(forms.ModelForm):
    class Meta:
        model = Transfers
        fields = ['transfer_title', 'source_warehouse', 'destination_warehouse', 'destination_unit', 'description']
        widgets = {
            'transfer_title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm rounded-2',
                'placeholder': 'عنوان درخواست انتقال کالا را وارد کنید...'
            }),
            'source_warehouse': forms.Select(attrs={
                'class': 'form-select form-select-sm rounded-2'
            }),
            'destination_warehouse': forms.Select(attrs={
                'class': 'form-select form-select-sm rounded-2'
            }),
            'destination_unit': forms.Select(attrs={
                'class': 'form-select form-select-sm rounded-2'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-control-sm rounded-2',
                'rows': 3,
                'placeholder': 'توضیحات و اقلام انتقالی...'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # فیلتر انبارهای قابل دسترس کاربر
        if user and not user.is_superuser:
            # اگر در مدل کاربر فیلدی مثل store، branch یا units دارید
            # به طور مثال اگر به Store رابطه مستقیم دارد یا از طریق شعبه:
            user_store = getattr(user, 'store', None) or getattr(user, 'branch', None)
            
            if user_store:
                # اگر کاربر به یک انبار/شعبه خاص وصل است، انبار مبدا را به همان محدود می‌کنیم
                self.fields['source_warehouse'].queryset = Store.objects.filter(id=user_store.id)
            else:
                self.fields['source_warehouse'].queryset = Store.objects.all()

            # انبار مقصد می‌تواند از کل انبارها یا شعب مجاز انتخاب شود
            self.fields['destination_warehouse'].queryset = Store.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source_warehouse')
        destination = cleaned_data.get('destination_warehouse')

        # جلوگیری از انتخاب انبار یکسان
        if source and destination and source == destination:
            raise forms.ValidationError("انبار مبدأ و انبار مقصد نمی‌توانند یکسان باشند.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        user_notes = instance.description or ""
        
        # ذخیره دقیق محتوا مطابق با الگوی درخواستی شما:
        # انتقالی
        # از انبار : ...
        # به انبار : ...
        formatted_desc = (
            f"انتقالی\n"
            f"از انبار : {instance.source_warehouse.name if hasattr(instance.source_warehouse, 'name') else instance.source_warehouse}\n"
            f"به انبار : {instance.destination_warehouse.name if hasattr(instance.destination_warehouse, 'name') else instance.destination_warehouse}"
        )
        if user_notes.strip():
            formatted_desc += f"\n\nشرح:\n{user_notes.strip()}"

        instance.description = formatted_desc

        if commit:
            instance.save()
        return instance
