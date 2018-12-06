from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


def upload_image_dir(user, filename):
    return u'profiles/%s/%s' % (str(user.id), str(user.username + '.' + filename.split('.')[-1]))


class User(AbstractUser):
    avatar = models.ImageField(upload_to=upload_image_dir, default=settings.DEFAULT_PHOTO_PROFIL, blank=True, null=True)
    email = models.EmailField(unique=True)
    LANGUAGE_CHOICES = (
        ('fr', 'Français'),
        ('en', 'English')
    )
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=3, default='fr')
    oauth = models.BooleanField(default=False)

    def __str__(self):
        return self.email


