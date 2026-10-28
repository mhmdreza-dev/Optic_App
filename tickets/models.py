from django.db import models
from accounts.models import User,Unit
from django.conf import settings
# -----------------------------
# مدل تیکت (Ticket)
# -----------------------------

class Ticket (models.Model):
    class Meta:
    # نام جدول در دیتابیس
        db_table = "tickets"
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    STATUS_CHOICES = (
        ("open", "باز"),
        ("progress", "در حال بررسی"),
        ("closed", "بسته"),
    )
    PRIORITY_CHOICES = (
        ('low','کم'),
        ('medium','متوسط'),
        ('top','بالا'),
        ('critical','بحرانی'),
    )

    ticket_number = models.PositiveIntegerField(
        unique=True,
        blank=True,
        verbose_name="شماره تیکت"
    )
    ticket_type = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='اولویت'

    )
    # عوان تیکت
    ticket_title = models.CharField(
        max_length= 100 ,
        verbose_name='عنوان تیکت'
        )
    
    #شرح تیکت
    description = models.TextField(
        verbose_name="شرح تیکت"
        )

    #واحد مقصد تیکت
    destination_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='units_ticket',
        verbose_name="واحد مقصد"
        )
    
    # ایجاد کننده تیکت
    creator = models.ForeignKey (
        User ,
        on_delete=models.PROTECT,
        related_name="created_tickets",
        verbose_name='ایجاد کننده'
        )

    # زمان ایجاد تیکت
    create_time =models.DateTimeField (auto_now_add=True ,verbose_name='تاریخ ایجاد')
    # بردارنده تیکت
    taken_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taken_tickets",
        verbose_name='بردارنده تیکت'
    )

    # زمان برداشتن تیکت
    taken_time = models.DateTimeField(null=True, blank=True ,verbose_name='زمان برداشتن تیکت') 
    # زمان پایان تیکت
    expiration_time = models.DateTimeField(null=True, blank=True ,verbose_name='زمان پایان تیکت')

    priority =models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='اولویت'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        verbose_name='وضعیت'
    )

    reference_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reference_to",
        verbose_name='ارجاع به'
        )
# -----------------------------
# مدل فایل ضمیمه (TicketAttachment)
# -----------------------------

class TicketAttachment(models.Model):


    class Meta:
        db_table = 'attachments'
        verbose_name = "ضمیمه"
        verbose_name_plural = "ضمیمه ها"    

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name='تیکت'
    )

    file = models.FileField(
        upload_to="tickets/ticket_attachments/"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for Ticket {self.ticket.id}"
    

# -----------------------------
# مدل پاسخ تیکت ها (TicketMessage)
# -----------------------------   

class TicketMessage(models.Model):

    class Meta :
        db_table = "ticketmessages"
        verbose_name = "پیام تیکت"
        verbose_name_plural = "پاسخ های تیکت"
    
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    content = models.TextField(verbose_name='متن')
    create_time = models.DateTimeField(auto_now_add=True ,verbose_name="زمان ایجاد")
    # این فیلد برای ریپلای به پاسخ‌هاست!
    reply_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='replies',
        verbose_name="پاسخ به"
    )
    def __str__(self):
        return f"پیام {self.id} در تیکت {self.ticket.id}"

    
# -----------------------------
# مدل نوتیفیکیشن ارجاع تیکت ها (TicketMessage)
# -----------------------------   

class TicketReferralNotification (models.Model):

    class Meta :
        db_table = "TicketReferralNotification"
        verbose_name = "نوتیفیکیشن ارجاع تیکت"
        verbose_name_plural = "نوتیفیکیشن ارجاع تیکت ها"

    ticket = models.ForeignKey(Ticket ,on_delete=models.CASCADE,related_name='Ticket_referral_notification')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE ,related_name='sender_user')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE ,related_name='recipient_user')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"اعلان برای {self.recipient} - تیکت {self.ticket_id}"