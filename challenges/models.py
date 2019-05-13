from django.db import models
from django.utils import timezone
from users.models import Developer, Clinician
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Challenge(models.Model):
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length=200, default="")
    date_created = models.DateTimeField(default=timezone.now)
    # award = RichTextUploadingField(blank=True)
    award = models.IntegerField(verbose_name= ('Target cost saving in GBP'), default=0, blank=True, validators=[MaxValueValidator(1000000000)])
    clinician = models.ForeignKey(Clinician, on_delete=models.CASCADE, related_name="creator")  # clinician who created the challenge
    developers = models.ManyToManyField(Developer, blank=True)  # developerS who indicated interest
    description = RichTextUploadingField(blank=True)
    evaluation = RichTextUploadingField(blank=True)
    timeline = RichTextUploadingField(blank=True)
    rule = RichTextUploadingField(blank=True)
    data = models.FileField(blank=True)

    def get_developers(self):
        return ",".join([str(d) for d in self.developers.all()])

    def __str__(self):
        return f'Challenge: {self.title}'

    def get_absolute_url(self):
        return reverse('challenges_detail', kwargs={'pk': self.pk})
