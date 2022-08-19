from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Clientele(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    full_name = models.CharField(max_length=250, null=False)
    phone_no = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)

    def __str__(self):
        return f"{self.full_name}"


class Password(models.Model):
    clientele = models.ForeignKey(Clientele, on_delete=models.CASCADE)
    recovery_password = models.CharField(max_length=12, null=False)
    time = models.DateTimeField(null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.clientele} -> {self.recovery_password}"

    def expiry(self):
        if (timezone.now() - self.time) >= timezone.timedelta(hours=1):
            self.delete()
        else:
            pass


class Account(models.Model):
    clientele = models.ForeignKey(Clientele, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ref_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_investments = models.IntegerField(default=0)
    active_investments = models.IntegerField(default=0)
    total_deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdrawal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.clientele} -> {self.balance}"


class Deposit(models.Model):
    clientele = models.ForeignKey(Clientele, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, null=False, choices=[
        ('BTC', 'BTC'),
        ('USDT', 'USDT'),
    ])
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.clientele} -> {self.amount}"


class Withdrawal(models.Model):
    clientele = models.ForeignKey(Clientele, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, null=False, choices=[
        ('BANK', 'BANK'),
        ('BTC', 'BTC'),
        ('USDT', 'USDT'),
    ])
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.clientele} -> {self.amount}"


class Investment(models.Model):
    clientele = models.ForeignKey(Clientele, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    plan = models.CharField(max_length=10, null=False, choices=[
        ('Basic', 'Basic'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    ])
    profit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.clientele} -> {self.plan}"


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)  # User
    referer = models.ForeignKey(Clientele, on_delete=models.CASCADE)  # Person who referred user
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField()

    def __str__(self):
        return f"{self.user} -> {self.referer}"

