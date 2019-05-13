from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Probably can do without separate models for Developer/Clinician/Admin as the boolean flag seems to suffice.
# Also, the need for an is_admin is questionable because I see no use case for it,
# not sure how real companies handle account with admin rights. Need to refactor these later


# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_clinician = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Clinician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="profile-pics/default.jpg", upload_to="profile-pics")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output = (300, 300)
            img.thumbnail(output)
            img.save(self.image.path)
