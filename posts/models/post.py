from django.db import models
from django.conf import settings
from django.utils import timezone
from PIL import Image
import os


class Post(models.Model):
    description = models.TextField(
        max_length=1000,
        verbose_name='Описание',
        null=False
    )
    image = models.ImageField(
        verbose_name='Фото',
        null=False,
        blank=True,
        upload_to='post_images'
    )
    image_square = models.ImageField(
        upload_to='post_images_square/',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        related_name='posts',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        null=False,
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время",
        null=True
    )

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            width, height = img.size
            min_size = min(width, height)
            left = (width - min_size) / 2
            top = (height - min_size) / 2
            right = (width + min_size) / 2
            bottom = (height + min_size) / 2
            img = img.crop((left, top, right, bottom))
            image_square_path = os.path.join('post_images_square/', os.path.basename(self.image.path))
            with open(os.path.join(settings.MEDIA_ROOT, image_square_path), 'wb') as f:
                img.save(f)
            self.image_square = image_square_path
            super().save(*args, **kwargs)
