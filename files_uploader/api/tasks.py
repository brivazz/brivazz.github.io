import mimetypes
import os
import shutil

from api.models import File
from celery import shared_task
from django.conf import settings
from PIL import Image


@shared_task
def process_file(file_id: int) -> None:
    try:
        file = File.objects.get(id=file_id)
        file_path = file.file.path

        mimetype, encoding = mimetypes.guess_type(file_path)
        if os.path.isfile(file_path):
            if mimetype and mimetype.startswith('image/'):
                # обработка изображений
                image = Image.open(file_path)
                image.thumbnail((800, 800))
                processed_file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
                image.save(processed_file_path)

            elif mimetype and mimetype.startswith('text/'):
                # обработка текстового файла
                processed_file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
                with open(file_path) as text_file:
                    content = text_file.read()
                    processed_content = content.upper()

                    with open(processed_file_path, 'w') as processed_file:
                        processed_file.write(processed_content)
            else:
                # обработка других типов файлов
                processed_file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
                shutil.copyfile(file_path, processed_file_path)

            file.processed = True
            file.save()
        else:
            raise FileNotFoundError(f'Файл не найден: {file_path}')

    except File.DoesNotExist:
        raise ValueError(f'Файл с ID {file_id} не найден')
