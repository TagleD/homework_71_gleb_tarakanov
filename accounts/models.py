from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from accounts.manager import UserManager
username_validator = UnicodeUsernameValidator()


class Account(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('N', 'Не указано'),
    )
    phone_regex = RegexValidator(
        regex=r'^\+7\d{10}$',
        message="Номер телефона должен быть в формате: '+77011112233'"
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        blank=False,
        null=False
    )
    avatar = models.ImageField(
        null=True,
        blank=False,
        upload_to='user_pic',
        verbose_name='Аватар',
        default=None
    )
    phone = models.CharField(
        max_length=15,
        validators=[phone_regex],
        verbose_name='Номер телефона',
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=500,
        null=True,
        verbose_name='Информация о пользователе'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='N',
        verbose_name='Пол',
    )
    liked_posts = models.ManyToManyField(
        verbose_name='Понравившиеся публикации',
        to='posts.Post',
        related_name='user_likes'
    )
    subscriptions = models.ManyToManyField(
        verbose_name='Подписки',
        to='accounts.Account',
        related_name='subscribers'
    )
    commented_posts = models.ManyToManyField(
        verbose_name='Прокомментированные посты',
        to='posts.Post',
        related_name='user_comments'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'avatar']

    objects = UserManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
