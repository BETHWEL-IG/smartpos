from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.product.price * self.quantity
        
        # Update product stock
        if self.pk is None:  # Only adjust stock for new sales
            if self.quantity > self.product.stock:
                raise ValueError("Not enough stock available.")
            self.product.stock -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - ${self.total_price}"

