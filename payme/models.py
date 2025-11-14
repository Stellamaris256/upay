from django.db import models
from django.contrib.auth.models import User 
from random import randint, choice
from string import ascii_lowercase


GENDER = (
    ("M", "MALE"),
    ("F", "FEMALE"),
    ("U", "UNSPECIFIED"),
)

TRANSACTION_TYPES = (
    ('withdraw', 'Withdraw'),
    ('transfer', 'Transfer'),
    ('deposit', 'Deposit'),
)


def generateTRansactionId():
    str_selection = ''.join(choice(ascii_lowercase) for _ in range(6))
    return f"trx-{randint(10000,99999)}{str_selection}{randint(10000,99999)}"

def generateAccountNumber():
    return str(randint(1000000000, 9999999999))


class Client(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=4, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, default="U")
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=1000.00)
    account_number = models.CharField(max_length=10, unique=True, default=generateAccountNumber)

    def __str__(self):
        return f'{self.user.username} {self.account_number} => NGN{self.balance}'


class Transaction(models.Model):
    initiator = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    receiver_account_number = models.CharField(max_length=10, blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='transfer')
    date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=40, unique=True, default=generateTRansactionId)

    def __str__(self):
        return f"{self.transaction_type.title()} of NGN{self.amount} by {self.initiator.user.username} on {self.date.strftime('%Y-%m-%d %H:%M:%S')}"


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, unique = True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

