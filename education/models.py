from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.
class TutorialCategory (models.Model):
    """سرفصل یا دسته‌بندی آموزش‌ها"""
    class Meta:
        verbose_name = "سرفصل آموزشی"
        verbose_name_plural = "سرفصل‌های آموزشی"
        ordering = ['id']

    title = models.CharField (max_length=50 , verbose_name='نام دسته بندی')
    description = models.TextField(blank=True, verbose_name="توضیحات")
    status = models.BooleanField (default= True ,verbose_name = 'وضعیت')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TutorialVideo (models.Model):
    """  فیلم های آموزشی"""
    class Meta:
        verbose_name = "ویدیو آموزشی"
        verbose_name_plural = "ویدیوهای آموزشی"
        ordering = ['id']

    title = models.CharField(max_length=200, verbose_name="عنوان آموزش")
    description = models.TextField(blank=True, verbose_name="توضیحات و نکات تکمیلی")
    category = models.ForeignKey(
        TutorialCategory, 
        on_delete=models.CASCADE, 
        related_name='videos',
        verbose_name="سرفصل"
    )
    video_file = models.FileField(
        upload_to='tutorials/videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'webm'])],
        verbose_name="فایل ویدیو (MP4/WebM)"
    )
    is_active = models.BooleanField(default=True, verbose_name= "وضعیت")

    def __str__(self):
        return f"{self.category.title} - {self.title}"