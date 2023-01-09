from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('profile/', profile, name="profile"),
    path('invest/', deposit, name="invest"),
    path('deposit/btc/', deposit_btc, name="btc"),
    path('deposit/eth/', deposit_eth, name="eth"),
    path('deposit/trc/', deposit_trc, name="trc"),
    path('withdraw/', withdraw, name="withdraw"),
    path('wallet/', wallet, name="wallet"),
    path('wallet/<int:pk>/delete/', del_wallet, name="del_wallet"),
    path('referrals/', my_referrals, name="referral"),
    path('logout/', logout_request, name="logout"),
    path('total_investments/', tot_deposit, name="tot_investment"),
    path('total_withdrawals/', tot_withdraw, name="tot_withdraw"),
    path('transfer/', transfer, name='transfer'),
    path('transfer/confirm/', confirm_transfer, name='confirm_transfer'),
    path('total_transfers/', tot_transfer, name='tot_transfer')
]