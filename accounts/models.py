from django.db import models

# Create your models here.
#class User_account(models.Model):
#    about = models.CharField(max_length=100)
#    location = models.CharField(max_length=100)
#    account_age = models.PositiveIntegerField(default=18)
#
#    select_gender = (
#        ('Other', 'Other'),
#        ('Male', 'Male'),
#        ('Female', 'Female'),)
#    gender = models.CharField(max_length=8, choices=select_gender, default="other")
#
#    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)