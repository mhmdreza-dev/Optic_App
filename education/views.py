from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from .models import TutorialCategory, TutorialVideo


@login_required
def education_home(request, video_id=None):
    # دسته‌های فعال + ویدیوهای فعال (پرفورمنس بهتر)
    categories = TutorialCategory.objects.filter(status=True).prefetch_related(
        Prefetch("videos", queryset=TutorialVideo.objects.filter(is_active=True).order_by("id"))
    ).order_by("id")

    current_video = None

    if video_id:
        current_video = get_object_or_404(
            TutorialVideo,
            id=video_id,
            is_active=True,
            category__status=True,
        )
    else:
        # اولین ویدیو از اولین دسته (اگر وجود داشته باشد)
        first_cat = categories.first()
        if first_cat:
            current_video = first_cat.videos.first()

    context = {
        "categories": categories,
        "current_video": current_video,
    }
    return render(request, "education/education_home.html", context)
