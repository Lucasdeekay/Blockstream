from django.contrib import admin

from UserAccount.models import Clientele, Password, Account, Deposit, Withdrawal, Investment, Referral


class ClienteleAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_no', 'email')


class PasswordAdmin(admin.ModelAdmin):
    list_display = ('clientele', 'recovery_password', 'time', 'is_active')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('clientele', 'balance', 'profit', 'bonus', 'ref_bonus',
                    'total_investments', 'active_investments', 'total_deposit', 'total_withdrawal')


class DepositAdmin(admin.ModelAdmin):
    list_display = ('clientele', 'mode', 'amount', 'date', 'is_verified')


class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('clientele', 'mode', 'amount', 'date', 'is_verified')


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('clientele', 'plan', 'profit', 'date', 'is_active')


class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'referer', 'bonus', 'date')


class EmailingAdmin(admin.ModelAdmin):
    list_display = ('clientele', 'emailOTP', 'emailProfit', 'emaiInvest')


admin.site.register(Clientele, ClienteleAdmin)
admin.site.register(Password, PasswordAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Referral, ReferralAdmin)
