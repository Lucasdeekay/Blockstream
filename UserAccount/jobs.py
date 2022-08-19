from django.shortcuts import get_object_or_404
from UserAccount.models import Clientele, Account, Investment, Deposit, Withdrawal


# Job updates the total and active investments made by clientele
def updateInvestmentDetails(user):
    # Get clientele
    clientele = get_object_or_404(Clientele, user=user)
    # Get clientele account
    account = get_object_or_404(Account, clientele=clientele)
    # Get clientele's investment details and calculate the amount of total and active investments
    account.total_investments = len(Investment.objects.filter(clientele=clientele))
    account.active_investments = len(Investment.objects.filter(clientele=clientele, is_active=True))


# Job updates the total deposits made by clientele
def updateDepositDetails(user):
    # Get clientele
    clientele = get_object_or_404(Clientele, user=user)
    # Get clientele account
    account = get_object_or_404(Account, clientele=clientele)
    # Get all the user deposit amount only and convert it into a list and sum it all up
    account.total_deposit = sum(Deposit.objects.filter(clientele=clientele).values_list('amount', flat=True))


# Job updates the total deposits made by clientele
def updateWithdrawalDetails(user):
    # Get clientele
    clientele = get_object_or_404(Clientele, user=user)
    # Get clientele account
    account = get_object_or_404(Account, clientele=clientele)
    # Get all the user deposit amount only and convert it into a list and sum it all up
    account.total_deposit = sum(Withdrawal.objects.filter(clientele=clientele).values_list('amount', flat=True))
