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
    balance = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    ref_bonus = models.FloatField(default=0)
    total_investments = models.IntegerField(default=0)
    active_investments = models.IntegerField(default=0)
    total_deposit = models.FloatField(default=0)
    total_withdrawal = models.FloatField(default=0)

    def __str__(self):
        return f"{self.clientele} -> {self.balance}"

    def update(self):
        self.total_investments = len(Investment.objects.filter(clientele=self.clientele))
        self.active_investments = len(Investment.objects.filter(clientele=self.clientele, is_active=True))
        self.profit += sum(Investment.objects.filter(clientele=self.clientele).values_list('profit', flat=True))
        self.total_deposit = sum(Deposit.objects.filter(clientele=self.clientele, is_verified=True).values_list('amount', flat=True))
        self.total_withdrawal = sum(Withdrawal.objects.filter(clientele=self.clientele, is_verified=True).values_list('amount', flat=True))
        self.ref_bonus = sum(Referral.objects.filter(referer=self.clientele).values_list('bonus', flat=True))


class Deposit(models.Model):
    clientele = models.ForeignKey(Clientele, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, null=False, choices=[
        ('BTC', 'BTC'),
        ('USDT', 'USDT'),
    ])
    amount = models.FloatField(default=0)
    date = models.DateTimeField()
    transaction_id = models.CharField(max_length=8)
    tid_confirmed = models.BooleanField(default=False)
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
    amount = models.FloatField(default=0)
    wallet = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField()
    otp = models.CharField(max_length=6)
    otp_confirmed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.clientele} -> {self.amount}"


class Investment(models.Model):
    clientele = models.ForeignKey(Clientele, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    plan = models.CharField(max_length=10, null=False, choices=[
        ('Basic', 'Basic'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    ])
    profit = models.FloatField(default=0)
    date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.clientele} -> {self.plan}"

    def expiry(self):
        if self.plan =='Basic':
            if (timezone.now() - self.date) >= timezone.timedelta(weeks=2):
                self.is_active = False
            else:
                pass
        elif self.plan =='Silver':
            if (timezone.now() - self.date) >= timezone.timedelta(weeks=4):
                self.is_active = False
            else:
                pass
        elif self.plan =='Gold':
            if (timezone.now() - self.date) >= timezone.timedelta(weeks=12):
                self.is_active = False
            else:
                pass
        else:
            if (timezone.now() - self.date) >= timezone.timedelta(weeks=24):
                self.is_active = False
            else:
                pass


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)  # User
    referer = models.ForeignKey(Clientele, on_delete=models.CASCADE)  # Person who referred user
    bonus = models.FloatField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} -> {self.referer}"

