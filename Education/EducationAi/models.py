from django.db import models

# Create your models here.


class user(models.Model):
    user_email = models.CharField(max_length=100,null=True)
    user_password = models.CharField(max_length=50,null=True)
    user_Address = models.CharField(max_length=50, null=True)
    user_country = models.CharField(max_length=50, null=True)
    user_plan = models.CharField(max_length=50, null=True)
    user_description = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.user_email
    