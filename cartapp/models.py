from django.db import models
from django.contrib.auth.models import User
class Contact(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField()
    desc=models.TextField(null=True)
    phone=models.IntegerField()
    def __str__(self):
        return (self.name)

class logo(models.Model):
    image=models.ImageField(upload_to='products/')

CATEGORY_CHOICES=(
    ('mobiles','mobiles'),
    ('laptops','laptops'),
    ('clothing','clothing')

)
class Product(models.Model):
    name=models.CharField(max_length=60)
    description=models.TextField(null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(choices=CATEGORY_CHOICES,default='mobiles',max_length=10)
    image=models.ImageField(upload_to='products/')
    def __str__(self):
        return (self.name)
class Cartitem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    def sub_total(self):
        return self.product.price*self.quantity
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    email=models.EmailField()
    phone=models.CharField(max_length=10)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    is_current_address = models.BooleanField(default=False)
    def __str__(self):
        return(self.email)
    
    

# Create your models here.
