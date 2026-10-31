from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone



# -----------------------------
# مدل شعبه (Branch)
# -----------------------------

class Branch(models.Model):
    class Meta:
        # نام جدول در دیتابیس
        db_table = "branches"
        verbose_name = "شعبه"
        verbose_name_plural = "شعب"
    # کد شعبه (باید یکتا باشد)
    branch_id = models.PositiveIntegerField(unique=True ,verbose_name= 'کد شعبه')

    # نام شعبه
    branch_name = models.CharField(max_length=150,verbose_name= 'نام شعبه')

    # تلفن
    phone = models.CharField(max_length=20,null=True,verbose_name= 'تلفن')

    #وضعیت
    status = models.BooleanField(default=True,verbose_name= 'فعال')

    # نمایش بهتر در Django Admin
    def __str__(self):
        return f"{self.branch_id}-{self.branch_name}"

# -----------------------------
# مدل انبار (Store)
# -----------------------------

class Store (models.Model):
    class Meta:
        db_table ='stores'
        verbose_name = 'انبار'
        verbose_name_plural = 'انبارها'
    
    #کد انبار
    store_id = models.PositiveIntegerField( unique=True ,verbose_name="کد انبار")
    #نام انبار
    store_name = models.CharField(max_length=100 ,verbose_name="نام انبار")
    #شعبه
    branch = models.ForeignKey(Branch,
                                on_delete=models.PROTECT,
                                related_name="Stores" ,
                                verbose_name="نام شعبه"
                                )
    #وضعیت
    is_active = models.BooleanField(default=True ,verbose_name="فعال")

    # نمایش بهتر در Django Admin
    def __str__(self):
        return f" {self.store_name}"
    
# -----------------------------
# مدل شعبه (Unit)
# -----------------------------
class Unit(models.Model):
    class Meta :
        db_table = 'units'
        verbose_name = 'واحد'
        verbose_name_plural = 'واحد ها'
    # کد واحد
    unit_id = models.PositiveIntegerField(unique=True ,verbose_name= 'کد واحد')
    #نام واحد
    unit_name = models.CharField(max_length=30 ,blank=False ,verbose_name='نام واحد')
    #وضعیت
    is_active = models.BooleanField(default=True ,verbose_name='فعال')

    def __str__(self):
        return f"{self.unit_name}"
# -----------------------------
# مدل سمت ها position
# -----------------------------

class Position (models.Model):

    class Meta :
        db_table = "positions"
        verbose_name = "سمت"
        verbose_name_plural = "سمت ها"

    #کد سمت
    position_id = models.PositiveIntegerField( unique=True , verbose_name= 'کد سمت')
    #نام سمت
    position_name = models.CharField(max_length=30 , verbose_name='نام سمت')

    def __str__(self):
        return self.position_name

# -----------------------------
# Manager مخصوص مدل User
# -----------------------------
class UserManager(BaseUserManager):

    def create_user(self, username, employee_code, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if password is None:
            raise ValueError("Password is required")

        user = self.model(
            username=username,
            employee_code=employee_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, employee_code, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if password is None:
            raise ValueError("Superuser must have a password")

        return self.create_user(username, employee_code, password, **extra_fields)


# -----------------------------
# مدل کاربر (User)
# -----------------------------
class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = "users"
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    # نکته: اگر می‌خواهی صفرهای ابتدایی employee_code حفظ شود،
    # آن را به CharField با RegexValidator عددی تغییر بده.
    employee_code = models.PositiveIntegerField(
        unique=True,
        verbose_name="کد کارمند"
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="نام کاربری"
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name="نام"
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name="نام خانوادگی"
    )

    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="تلفن همراه"
    )

    phoneextensions = models.CharField(
        max_length=5,
        unique=True,
        verbose_name="داخلی"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="ایمیل"
    )

    # سمت سازمانی (رابطه معکوس صحیح: position.users)
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="users",
        verbose_name="سمت"
    )

    # ارتباط کاربر با شعبه (اختیاری)
    branch = models.ForeignKey(
        'Branch',  # یا Branch اگر بالاتر تعریف شده
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="users",
        verbose_name="شعبه"
    )

    # واحد کاربر (اجباری)
    unit = models.ForeignKey(
        'Unit',  # یا Unit اگر بالاتر تعریف شده
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="users",
        verbose_name="واحد"
    )

    profile_image = models.ImageField(upload_to="accounts/profile_image/",
                                      null=True ,
                                      blank=True,
                                      verbose_name="تصویر پروفایل"   
                                    
                                     )
    user_signature =models.ImageField(
        upload_to="accounts/user_signature/",
        null=True,
        blank=True,
        verbose_name= "امضا کاربر"
    )

    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_staff = models.BooleanField(default=False, verbose_name="کارمند (دسترسی پنل)")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["employee_code"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username