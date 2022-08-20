from django.urls import path, include
from rest_framework import routers

from UserAccount import views
from UserAccount.api_views import ClienteleView, PasswordView, AccountView, DepositView, WithdrawalView, InvestmentView, \
    ReferralView

app_name = 'UserAccount'

router = routers.DefaultRouter()
router.register('clientele', ClienteleView)
router.register('password', PasswordView)
router.register('account', AccountView)
router.register('deposit', DepositView)
router.register('withdrawal', WithdrawalView)
router.register('investment', InvestmentView)
router.register('referral', ReferralView)

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.log_in, name='login'),
    path('login/forgot-password', views.forgotten_password, name='forgot_password'),
    path('login/forgot-password/<int:clientele_id>/retrieve-password', views.password_retrieval, name='password_retrieval'),
    path('login/forgot-password/<int:clientele_id>/resend-password', views.resend_password,
         name='resend_password'),
    path('<int:clientele_id>/retrieve-password/update-password', views.update_password, name='update_password'),
    path('logout', views.log_out, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('deposit', views.deposit, name='deposit'),
    path('deposit/wallet/<str:mode>', views.wallet, name='wallet'),
    path('invest', views.invest, name='invest'),
    path('withdraw-fund', views.withdraw, name='withdraw'),
    path('withdraw-fund/verify', views.confirm_withdrawal, name='confirm_withdrawal'),
    path('profit-record', views.profit_record, name='profit_record'),
    path('transaction', views.transaction, name='transaction'),
    path('refer', views.refer, name='refer'),
    path('refer/<str:ref>', views.ref_register, name='ref_register'),
    path('support', views.support, name='support'),
    path('settings', views.settings, name='settings'),
    path('api/', include(router.urls))
]
