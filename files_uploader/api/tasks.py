import mimetypes
import os
import shutil

from api.models import File
from celery import shared_task
from django.conf import settings
from PIL import Image


def process_image(file_path: str, processed_file_path: str) -> None:
    """Обрабатывает изображение с указанным путем `file_path`.

        Сохраняет файл по новому пути `processed_file_path`.

    Args:
        file_path (str): Путь к исходному файлу изображения.
        processed_file_path (str): Путь для сохранения обработанного изображения.
    """
    image = Image.open(file_path)
    image.thumbnail((800, 800))
    image.save(processed_file_path)


def process_text(file_path: str, processed_file_path: str) -> None:
    """Обрабатывает текстовый файл с указанным путем `file_path`.

        Сохраняет файл по новому пути `processed_file_path`,
        переводя содержимое текста в верхний регистр.

    Args:
        file_path (str): Путь к исходному текстовому файлу.
        processed_file_path (str): Путь для сохранения обработанного текстового файла.
    """
    with open(file_path) as text_file:
        content = text_file.read()
        processed_content = content.upper()
        with open(processed_file_path, 'w') as processed_file:
            processed_file.write(processed_content)


def process_other(file_path: str, processed_file_path: str) -> None:
    """Копирует файл с указанным путем `file_path`.

        Сохраняет копию файла в новом месте `processed_file_path`.
        Предназначено для обработки файлов других типов,
        не являющихся изображениями или текстовыми файлами.

    Args:
        file_path (str): Путь к исходному файлу.
        processed_file_path (str): Путь для сохранения скопированного файла.
    """
    shutil.copyfile(file_path, processed_file_path)


@shared_task
def process_file(file_id: int) -> None:
    """Основная функция для обработки файлов.

    Args:
        file_id (int): ID файлa в бд.
    """
    try:
        file = File.objects.get(id=file_id)
        file_path = file.file.path

        mimetype, encoding = mimetypes.guess_type(file_path)
        if os.path.isfile(file_path):
            processed_file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

            if mimetype and mimetype.startswith('image/'):
                # обработка изображений
                process_image(file_path, processed_file_path)

            elif mimetype and mimetype.startswith('text/'):
                # обработка текстового файла
                process_text(file_path, processed_file_path)

            else:
                # обработка других типов файлов
                process_other(file_path, processed_file_path)

            file.processed = True
            file.save()
        else:
            raise FileNotFoundError(f'Файл не найден: {file_path}')

    except File.DoesNotExist:
        raise ValueError(f'Файл с ID {file_id} не найден')
