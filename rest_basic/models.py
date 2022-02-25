from django.db import models

# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=300)
    author=models.CharField(max_length=300)
    email=models.EmailField(max_length=100)
    date=models.DateField(auto_now_add=True)


    def __str__(self):
        self.author