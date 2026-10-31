from django import forms
from .models import Transfers
from accounts.models import Store, Unit

class NewTransferForm(forms.ModelForm):
    class Meta:
        model = Transfers
        fields = [
            'transfer_title',
            'source_warehouse',
            'destination_warehouse',
            'destination_unit',
            'description'
        ]
        widgets = {
            'transfer_title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm rounded-2',
                'placeholder': 'عنوان درخواست انتقال کالا را وارد کنید...'
            }),
            'source_warehouse': forms.Select(attrs={
                'class': 'form-select form-select-sm rounded-2 select2-searchable'
            }),
            'destination_warehouse': forms.Select(attrs={
                'class': 'form-select form-select-sm rounded-2 select2-searchable'
            }),
            'destination_unit': forms.Select(attrs={
                'class': 'form-select form-select-sm rounded-2 select2-searchable'
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

        # تنظیم متن پیش‌فرض برای گزینه‌ها
        self.fields['source_warehouse'].empty_label = "--- انتخاب انبار مبدأ ---"
        self.fields['destination_warehouse'].empty_label = "--- انتخاب انبار مقصد ---"
        self.fields['destination_unit'].empty_label = "--- انتخاب واحد مقصد (اختیاری) ---"
        self.fields['destination_unit'].required = False

        # فیلتر انبارهای مبدأ بر اساس کاربر / شعبه
        if user:
            if not user.is_superuser and hasattr(user, 'branch') and user.branch:
                allowed_stores = Store.objects.filter(branch=user.branch)
                self.fields['source_warehouse'].queryset = allowed_stores

                # اگر کاربر فقط به یک انبار دسترسی دارد، خودکار انتخاب شود
                if allowed_stores.count() == 1:
                    self.fields['source_warehouse'].initial = allowed_stores.first()
            else:
                self.fields['source_warehouse'].queryset = Store.objects.all()

        # لیست تمام انبارهای مقصد
        self.fields['destination_warehouse'].queryset = Store.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source_warehouse')
        destination = cleaned_data.get('destination_warehouse')

        # جلوگیری از یکی بودن مبدا و مقصد و الصاق مستقیم ارور به فیلد مقصد
        if source and destination and source == destination:
            self.add_error(
                'destination_warehouse',
                'انبار مقصد نمی‌تواند همان انبار مبدأ باشد.'
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        user_notes = (instance.description or "").strip()

        source_name = getattr(instance.source_warehouse, 'name', str(instance.source_warehouse))
        dest_name = getattr(instance.destination_warehouse, 'name', str(instance.destination_warehouse))

        # ایجاد ساختار متنی خودکار
        header_text = f"انتقالی\nاز انبار : {source_name}\nبه انبار : {dest_name}"

        # اگر متن از قبل همین الگو را نداشت، آن را بچسباند (برای جلوگیری از تکرار مجدد)
        if not user_notes.startswith("انتقالی"):
            if user_notes:
                instance.description = f"{header_text}\n\nشرح:\n{user_notes}"
            else:
                instance.description = header_text

        if commit:
            instance.save()
        return instance
