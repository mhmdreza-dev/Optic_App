from django import forms
from .models import Transfers
from accounts.models import Store, Unit ,User
from django import forms
from products.models import Product  # نام اپ خودتان را بگذارید
from django.forms import inlineformset_factory
from .models import Transfers, TransferItems
# فرم ایجاد انتقالی
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
        # 1. استخراج کاربر از ورودی‌ها
        self.user = kwargs.pop('user', None)
        
        # 2. فراخوانی سازنده اصلی جنگو
        super().__init__(*args, **kwargs)
        
        # 3. تنظیم متون پیش‌فرض گزینه‌ها (از متد اول شما)
        self.fields['source_warehouse'].empty_label = "--- انتخاب انبار مبدأ ---"
        self.fields['destination_warehouse'].empty_label = "--- انتخاب انبار مقصد ---"
        self.fields['destination_unit'].empty_label = "--- انتخاب واحد مقصد (اختیاری) ---"
        self.fields['destination_unit'].required = False  # قبلاً ارور نال داشت، اینجا باید اختیاری (False) باشد

        # 4. بررسی لاگ کاربر در ترمینال
        print("کاربر در فرم دریافت شد:", self.user)

        # 5. فیلتر کردن انبار مبدأ بر اساس شعبه کاربر
        if self.user and hasattr(self.user, 'branch') and self.user.branch:
            user_branch = self.user.branch
            self.fields['source_warehouse'].queryset = Store.objects.filter(branch=user_branch)
            self.fields['destination_warehouse'].queryset = Store.objects.filter(branch=user_branch)


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


# فرم انخاب کالای انتقالی
# inventory/forms.py




class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # نمایش کد و نام کالا در لیست گزینه‌ها
        return f"{obj.productid} — {obj.productname}"


class TransferItemForm(forms.ModelForm):
    product = ProductChoiceField(
        queryset=Product.objects.all().order_by("productname"),
        empty_label="--- انتخاب کالا یا کد ---",
        label="کالا و کد",
        widget=forms.Select(
            attrs={
                # کلاس select2-product برای فعال‌سازی جستجو با JS
                "class": "form-select select2-product",
                "style": "width: 100%;",
            }
        ),
    )

    class Meta:
        model = TransferItems
        fields = ["product", "unit", "quantity", "consumer_price"]
        widgets = {
            "unit": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.001",
                    "min": "0.001",
                    "placeholder": "مقدار",
                }
            ),
            "unit_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "1",
                    "min": "0",
                    "placeholder": "قیمت واحد",
                }
            ),
            "consumer_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "1",
                    "min": "0",
                    "placeholder": "قیمت واحد",
                }
            ),
        }


TransferItemFormSet = inlineformset_factory(
    Transfers,
    TransferItems,
    form=TransferItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)