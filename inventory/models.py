from django.db import models
from accounts.models import User ,Unit ,Store
# Create your models here.

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
