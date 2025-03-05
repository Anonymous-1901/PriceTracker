from django.contrib.auth.models import User
from django.db import models

class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255,default='Default Product')
    product_url = models.URLField()  # Storing the product URL directly
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)  # Desired target price for the alert
    is_active = models.BooleanField(default=True)  # To mark if the alert is still active
    alert_sent = models.BooleanField(default=False)  # Whether an alert has been sent
    product_image_url = models.CharField(max_length=255,default='')
    
    def __str__(self):
        return f"{self.user.username} alert for {self.product_url}"
