from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="users/user_img/", null=True, blank=True)

    def __str__(self):
        return self.username


