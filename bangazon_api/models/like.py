from django.db import models
from django.contrib.auth.models import User


class Like(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} liked by {self.customer.get_full_name()}'
