from django.db import models
from django.conf import settings
from django.utils import timezone


class Comment(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор',
        to=settings.AUTH_USER_MODEL,
        related_name='comments',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        to='posts.Post',
        verbose_name='Публикация',
        related_name='comments',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Комментарий',
        null=False,
        blank=False
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        null=False,
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name="Время создания",
        default=timezone.now
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
