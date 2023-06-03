from django.db import models
from django.contrib.auth.models import User
from PIL import Image
User._meta.get_field('email')._unique = True

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    candidate_name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)
    logo = models.ImageField(upload_to='profile_Pics')
    bio = models.TextField()
    image = models.ImageField(upload_to='profile_Pics')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.choice_text
