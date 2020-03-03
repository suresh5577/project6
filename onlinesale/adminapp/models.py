from django.db import models

class Admin(models.Model):
    username=models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Merchant(models.Model):
    merchant_id = models.AutoField(primary_key=True)
    merchant_name = models.CharField(max_length=100)
    merchant_email = models.EmailField(unique=True)
    merchant_contact_no = models.IntegerField(unique=True)
    merchant_password = models.CharField(max_length=20)

    def __str__(self):
        return self.merchant_name

class Product(models.Model):
    prod_id = models.IntegerField(primary_key=True)
    prod_name = models.CharField(max_length=100)
    prod_price = models.FloatField()
    prod_qty = models.IntegerField()
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE)