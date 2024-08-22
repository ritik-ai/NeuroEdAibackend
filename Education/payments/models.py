
from django.db import models

# Create your models here.



class Subscription(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    paypal_subscription_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
