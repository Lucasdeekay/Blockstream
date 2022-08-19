from rest_framework import viewsets

from UserAccount.models import Clientele, Password, Account, Deposit, Withdrawal, Investment, Referral
from UserAccount.serializers import ClienteleSerializer, PasswordSerializer, AccountSerializer, DepositSerializer, \
    WithdrawalSerializer, InvestmentSerializer, ReferralSerializer


class ClienteleView(viewsets.ModelViewSet):
    serializer_class = ClienteleSerializer
    queryset = Clientele.objects.all()


class PasswordView(viewsets.ModelViewSet):
    serializer_class = PasswordSerializer
    queryset = Password.objects.all()


class AccountView(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class DepositView(viewsets.ModelViewSet):
    serializer_class = DepositSerializer
    queryset = Deposit.objects.all()


class WithdrawalView(viewsets.ModelViewSet):
    serializer_class = WithdrawalSerializer
    queryset = Withdrawal.objects.all()


class InvestmentView(viewsets.ModelViewSet):
    serializer_class = InvestmentSerializer
    queryset = Investment.objects.all()


class ReferralView(viewsets.ModelViewSet):
    serializer_class = ReferralSerializer
    queryset = Referral.objects.all()

