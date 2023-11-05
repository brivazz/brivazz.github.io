import os

from celery import shared_task
from django.conf import settings
from PIL import Image

from api.models import File


@shared_task
def process_file(file_id):
    file = File.objects.get(id=file_id)
    file_path = file.file.path
    file_extension = os.path.splitext(file_path)[1]

    if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        image = Image.open(file_path)
        image.thumbnail((800, 800))
        processed_file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        image.save(processed_file_path)
        file.processed_path = processed_file_path
    else:
        file.processed_path = file_path

    file.processed = True
    file.save()
