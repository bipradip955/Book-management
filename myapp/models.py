from django.db import models
from django import forms

# Create your models here.

class user(models.Model):

    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=50)
    book_type = models.CharField(max_length=30)
    author = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering = ['-id']
    




    
