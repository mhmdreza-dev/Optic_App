from django.db import models

class Product(models.Model):

    class Meta:
        managed = False          # بسیار مهم: جلوگیری از ساخت یا تغییر جدول توسط جنگو
        db_table = 'products'    # نام دقیق جدول در PostgreSQL
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    productid = models.IntegerField(primary_key=True, db_column='productid', verbose_name='شناسه کالا')
    productname = models.CharField(max_length=100, db_column='productname', verbose_name='نام کالا')
    mainunit = models.CharField(max_length=10, db_column='mainunit', verbose_name='واحد سنجش اصلی')
    status = models.CharField(max_length=8, db_column='status', verbose_name='وضعیت')
    
    # قیمت‌های ورودی
    consumer_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, db_column='consumer_price', verbose_name='قیمت مصرف‌کننده')
    manufacturer_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, db_column='manufacturer_price', verbose_name='قیمت تولیدکننده')
    
    # فیلدهای محاسباتی Postgres (صرفاً خواندنی - editable=False)
    selling_price = models.IntegerField(null=True, blank=True, editable=False, db_column='selling_price', verbose_name='قیمت فروش')
    paladium_price = models.IntegerField(null=True, blank=True, editable=False, db_column='paladium_price', verbose_name='قیمت پالادیوم')
    amiran_price = models.IntegerField(null=True, blank=True, editable=False, db_column='amiran_price', verbose_name='قیمت امیران')
    khalijfars_price = models.IntegerField(null=True, blank=True, editable=False, db_column='khalijfars_price', verbose_name='قیمت خلیج فارس')
    prisons_price = models.IntegerField(null=True, blank=True, editable=False, db_column='prisons_price', verbose_name='قیمت ندامتگاه‌ها')
    schools_price = models.IntegerField(null=True, blank=True, editable=False, db_column='schools_price', verbose_name='قیمت مدارس')
    hyperc_price = models.IntegerField(null=True, blank=True, editable=False, db_column='hyperc_price', verbose_name='قیمت هایپر سی')
    najm_price = models.IntegerField(null=True, blank=True, editable=False, db_column='najm_price', verbose_name='قیمت نجم')
    snap_price = models.IntegerField(null=True, blank=True, editable=False, db_column='snap_price', verbose_name='قیمت اسنپ')
    hyperahmadi_price = models.IntegerField(null=True, blank=True, editable=False, db_column='hyperahmadi_price', verbose_name='قیمت هایپر احمدی')
    digikala_price = models.IntegerField(null=True, blank=True, editable=False, db_column='digikala_price', verbose_name='قیمت دیجی‌کالا')



    def __str__(self):
        return f"{self.productname} ({self.productid})"
