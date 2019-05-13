from django.db import models
from django.utils import timezone
from users.models import Developer, Clinician
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Discussion(models.Model):
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    content = RichTextUploadingField()
    author = models.ForeignKey(Developer, on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('discussion_detail', kwargs={'pk': self.pk}) 
    
    def __str__(self):
        return f'Discussion: {self.title}'

    def get_author(self):
        return f'Discussion: {self.author}'


class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    date_commented = models.DateTimeField(default=timezone.now)
    content = models.TextField(default="")
    commenter = models.ForeignKey(Developer, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Comment by:: {self.commenter}'

    def get_discussion_title(self):
        return f'Commented on discussion: {self.discussion.title}'







    

