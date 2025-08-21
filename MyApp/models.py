from django.db import models

# Create your models here.
class userDatas(models.Model):
    full_name = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15,unique=True)
    password = models.CharField(max_length=128)
    date = models.DateField(auto_now_add=True)
    
    isblocked = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
class task(models.Model):
    user = models.ForeignKey(userDatas,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    category = models.CharField(max_length=50)
    important = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    