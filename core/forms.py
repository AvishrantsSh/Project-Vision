from django import forms
from core.models import VideoData

class VideoDataForm(forms.ModelForm):
    class Meta:
        model = VideoData
        fields =('video',)