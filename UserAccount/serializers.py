from rest_framework import serializers
from UserAccount.models import Clientele, Password, Account, Deposit, Withdrawal, Investment, Referral


class ClienteleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientele
        fields = "__all__"


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = "__all__"


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = "__all__"
