from django.db import models
from accounts.models import User ,Unit ,Store

# Create your models here.


#کلاس مدل انتقالی 
class Transfers (models.Model):

    class Meta:
        db_table ='transfers'
        verbose_name = 'انتقالی'
        verbose_name_plural = 'انتقالی ها'


    # عوان انتقالی
    transfer_title = models.CharField(
                                    max_length= 100 ,
                                    verbose_name='عنوان انتقالی'
                                    )

    #شرح انتقالی
    description = models.TextField(
                                    verbose_name="شرح انتقالی"
                                    )

    # انبار مبدا
    source_warehouse = models.ForeignKey(
                                        Store ,
                                        on_delete= models.CASCADE ,
                                        related_name = 'source_warehouse',
                                        verbose_name = 'انبار مبدا' ,
                                        )

    # انبار مقصد
    destination_warehouse = models.ForeignKey(
                                        Store ,
                                        on_delete= models.CASCADE ,
                                        related_name = 'destination_warehouse',
                                        verbose_name = 'انبار مقصد' ,
                                        )
    
    # ایجاد کننده انتقالی
    creator = models.ForeignKey(
                                User ,
                                on_delete=models.CASCADE ,
                                related_name='creator' ,
                                verbose_name='ایجاد کننده'
                                )
    
    # واحد مقصد
    destination_unit = models.ForeignKey( 
                                        Unit,
                                        on_delete=models.CASCADE,
                                        related_name='transfer_unit',
                                        verbose_name="واحد مقصد"
                                        )

    # بردارنده تیکت
    taken_by = models.ForeignKey(
                                User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name="taken_transfer",
                                verbose_name='بردارنده تیکت'    
                                )
    
    # ارجاع به
    reference_to = models.ForeignKey(
                                    User,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name="transfer_reference_to",
                                    verbose_name='ارجاع به'
                                    )
    
    # زمان ایجاد تیکت
    create_time =models.DateTimeField (
                                        auto_now_add=True ,
                                        verbose_name='تاریخ ایجاد'
                                       )
    
    # زمان برداشتن انتقالی
    taken_time = models.DateTimeField(
                                        null=True , 
                                        blank=True ,
                                        verbose_name='زمان برداشتن تیکت'
                                      ) 
    
    # زمان پایان انتقالی
    expiration_time = models.DateTimeField(
                                            null=True, 
                                            blank=True ,
                                            verbose_name='زمان پایان تیکت'
                                           )

# کلاس مدل آیتم های انتقالی
class TransferItems (models.Model):

    class Meta :
        db_table = 'transferitem'
        verbose_name = 'آتیم انتقالی'
        verbose_name_plural = 'آیتم های انتقالی'
        
    UNIT_CHOICES = [
                    ("number", "عدد"),
                    ("box", "جعبه"),
                    ("carton", "کارتن"),
                ]
    # ارتباط با مدل انتقلی
    transfer = models.ForeignKey(
        "Transfers",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="انتقالی",
    )
    # ارتباط با مدل کالا ها
    product = models.ForeignKey(
        "products.Product",  # نام مدل unmanaged کالاهای شما
        on_delete=models.PROTECT,
        to_field='productid', # صراحتاً بگویید به productid وصل شود
        db_column="product_id",
        verbose_name="کالا",
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        verbose_name="واحد سنجش",
    )

    quantity = models.IntegerField(
        verbose_name="تعداد",
    )

    consumer_price = models.IntegerField(
        verbose_name="قیمت مصرف کننده",
    )


    def __str__(self):
        return f"{self.product} - {self.quantity} {self.unit}"
