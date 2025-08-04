# from django.db import models
# from users.models import User

# # Create your models here.
# class ShippingAddress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)
#     country = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.user} - {self.address}"

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_paid = models.BooleanField(default=False)
#     is_delivered = models.BooleanField(default=False)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"Order #{self.pk} by {self.user}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"
