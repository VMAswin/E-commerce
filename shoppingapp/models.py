from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_Name=models.CharField(max_length=255)
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    prname=models.CharField(max_length=255)
    prprice=models.IntegerField()
    prdesc=models.CharField(max_length=255)
    primg=models.ImageField(upload_to="image/",null=True)
class userdetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255)
    number=models.CharField(max_length=255)
    usimg=models.ImageField(upload_to="image/",null=True)
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    prod=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=1)
    def total_price(self):
        return self.quantity*self.prod.prprice
