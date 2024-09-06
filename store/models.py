from django.db import models


class Product(models.Model) :
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now= True)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOISES = [
        (MEMBERSHIP_GOLD, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Solver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique= True)
    phone = models.CharField(max_length=12)
    birth_date = models.DateField(null=True)

class Order(models.Model):
    PAYMENT_PENDING = "P"
    PAYMENT_COMPLETE = "C"
    PAYMENT_FAILED = "F"

    PAYMENT_STATUS = [
        (PAYMENT_COMPLETE, "Complete"),
        (PAYMENT_PENDING, "Pending"),
        (PAYMENT_FAILED, "failed")
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,  choices=PAYMENT_STATUS, default=PAYMENT_PENDING)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)