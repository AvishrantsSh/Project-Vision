from celery import shared_task
from core.models import VideoData
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from backend.settings import EMAIL_CONF, DEFAULT_FROM_EMAIL, MODEL_PATH
import tflite_runtime.interpreter as tflite
from tensorflow import keras

@shared_task
def analyze_video(video_id):
    try:
        video = VideoData.objects.get(video_id=video_id)
    except VideoData.DoesNotExist:
        return False

    # Tensorflow logic start
    model = keras.models.load_model(MODEL_PATH)

    # Tensorflow logic end

    send_video_feedback_email({
        "email": video.user_id.email,
        "video_id": video.video_id,
        })

    return True

@shared_task
def send_video_feedback_email(context):
    config = EMAIL_CONF["SEND_VIDEO_FEEDBACK"]
    message = render_to_string(config["TEMPLATE"], context)
    video = VideoData.objects.get(video_id=context["video_id"])

    mail = EmailMessage(
        subject=config["SUBJECT"],
        body=message,
        from_email=DEFAULT_FROM_EMAIL,
        to=[context["email"]],
    )

    mail.content_subtype = "html"
    mail.attach(video.filename, video.video.read())
    mail.send()