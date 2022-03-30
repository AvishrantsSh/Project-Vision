from django.shortcuts import render
from core.forms import VideoDataForm
from core.models import VideoData
from core.tasks import analyze_video

def HomeView(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = VideoDataForm(request.POST, request.FILES)
        if form.is_valid():
            video = VideoData.objects.create(**{"user_id": request.user, "video": form.cleaned_data["video"]})
            analyze_video.delay(video.video_id)

    else:
        form = VideoDataForm()
        return render(request, 'home.html', {'form': form})

    return render(request, "home.html")
