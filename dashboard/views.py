from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password

from decimal import Decimal
from PIL import Image
import qrcode

from main.models import Site
from dashboard.models import (Subscription, Withdrawal, Plan,
                              Wallet, Transfer)
from .forms import (BasicInfo, AddressInfo, DeleteAccount,
                    DepositForm, WalletForm, WithdrawalForm,
                    TransferForm)
from account.models import Referral
from rsfholdings import settings


UserModel = get_user_model()

# Create your views here.


@login_required(login_url='account:login')
def dashboard(request):
    user = UserModel.objects.get(pk=request.user.pk)
    last_deposit = Subscription.objects.filter(
        user=user, active=True).last()
    last_withdrawal = Withdrawal.objects.filter(
        user=user, status="Confirmed").last()
    deposit = Subscription.objects.all()
    withdrawal = Withdrawal.objects.all()

    # TOTAL DEPOSITS
    tot_deposit = sum(
        [i.sub_amount for i in deposit if i.user == user and i.active == True])
    # ACTIVE DEPOSITS
    active_deposit = sum(
        [i.sub_amount for i in deposit if i.user == user and i.status == "Confirmed"])
    # TOTAL WITHDRAWALS
    tot_withdraw = sum(
        [i.amount for i in withdrawal if i.user == user and i.status == "Confirmed"])
    # PENDING WITHDRAWALS
    pend_withdraw = sum(
        [i.amount for i in withdrawal if i.user == user and i.status == "Pending"])
    # TOTAL BALANCE
    total_balance = user.balance
    # EARNED PROFIT TOTAL
    earned_total = user.profit

    context = {
        'tot_bal': total_balance,
        'tot_earned': earned_total,
        'last_deposit': last_deposit,
        'tot_deposit': tot_deposit,
        'active_deposit': active_deposit,
        'last_withdraw': last_withdrawal,
        'pend_withdraw': pend_withdraw,
        'tot_withdraw': tot_withdraw,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='account:login')
def profile(request):
    """Update User's Profile"""
    basic_info = BasicInfo(instance=request.user)
    address_info = AddressInfo(instance=request.user)
    delete_account = DeleteAccount(instance=request.user)

    if request.method == 'POST':
        if "form1" in request.POST:
            basic_info = BasicInfo(request.POST, instance=request.user)

            if basic_info.is_valid():
                basic_info.save()
                messages.success(
                    request, ("Your <b>Basic info</b> has been updated!"))
                return redirect('dashboard:profile')

        if 'form2' in request.POST:
            address_info = AddressInfo(request.POST, instance=request.user)
            if address_info.is_valid():
                address_info.save()
                messages.success(
                    request, ("Your <b>Address info</b> has updated!"))
                return redirect('dashboard:profile')

        if 'form3' in request.POST:
            delete_account = DeleteAccount(request.POST, instance=request.user)
            if delete_account.is_valid():
                deactivate_user = delete_account.save(commit=False)
                del_user = delete_account.cleaned_data['del_account']
                deactivate_user.save()
                if del_user:
                    messages.info(request, ("Your account has been deactivated. \n \
                                            Contact us for reactivation."))
                    # SEND MAIL
                    return redirect('main:contact')

    context = {
        'basic_info': basic_info,
        'address_info': address_info,
        'delete_account': delete_account
    }
    return render(request, 'dashboard/profile.html', context)

# Helper Function


def get_ip_address(request):
    """Function to get user's ip address"""
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')

    if user_ip_address:
        ip = user_ip_address.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', None)

    return ip


@login_required(login_url='account:login')
def deposit(request):
    """Function to allow investors make deposit"""
    user = get_object_or_404(UserModel, pk=request.user.pk)
    subscription = Subscription(user=user)
    plans = Plan.objects.all()

    if request.method == 'POST':
        form = DepositForm(request.POST, instance=subscription)

        if form.is_valid():
            subscribe = form.save(commit=False)
            method = form.cleaned_data['sub_method']
            currency = form.cleaned_data['sub_currency']
            amount = form.cleaned_data['sub_amount']

            if method == "Account":
                subscribe.active = True
                subscribe.save()
                # TODO: SEND CONFIRMATION MAIL TO ADMIN
                admin_msg = f'Hello Admin,\n\n{user.username.capitalize()} just subscribed to {subscription.plan} with an amount of ${amount} via {subscription.get_sub_currency_display()}.'
                admin_msg += f'\n\n{user.username.capitalize()} paid through his/her available Account Balance, and the package was automatically activated by the system.'
                admin_msg += f'\nNo further action is required of you.'
                admin_msg += f'\n\nRegards,\nDevTeam.'
                message1 = EmailMessage(
                    subject=f"User Investment Notification",
                    body=admin_msg,
                    from_email='settings.EMAIL_HOST_USER',
                    to=['okonkwogodspower@yahoo.com'],
                )
                message1.send(fail_silently=True)
                messages.success(
                    request, ("Transaction Successful. Your investment package will be activated shortly!"))
                return redirect('dashboard:tot_investment')
            else:
                subscribe.save()
                # TODO: SEND CONFIRMATION MAIL TO USER
                name = user.username
                context = ({
                    'user': name,
                    'amount': amount,
                    'currency': currency
                })
                html_version = './dashboard/mails/inactive_dep.html'
                html_message = render_to_string(html_version, context)
                subject = 'siteName - Investment Package Initiated'
                message = EmailMessage(
                    subject, html_message, settings.EMAIL_HOST_USER, [user.email])
                message.content_subtype = 'html'
                message.send(fail_silently=True)
                # TODO: SEND CONFIRMATION MAIL TO ADMIN
                admin_msg = f'Hello Admin,\n\n{name.capitalize()} just initiated a deposit request of ${amount} via {subscription.get_sub_currency_display()}.'
                admin_msg += f'\n\nKindly keep an eye out for the deposit, and confirm the transaction in the admin portal.'
                admin_msg += f'\nTo do that, navigate to the Subscription table, click on the user and toggle on the active button.\nOnce that is done, the plan will be automatically activated.'
                admin_msg += f'\n\nRegards,\nDevTeam.'
                message1 = EmailMessage(
                    subject=f"User Deposit Notification",
                    body=admin_msg,
                    from_email='settings.EMAIL_HOST_USER',
                    to=['okonkwogodspower@yahoo.com'],
                )
                message1.send(fail_silently=True)

                if currency == "Btc":
                    return redirect('dashboard:btc')
                elif currency == "Eth":
                    return redirect('dashboard:eth')
                else:
                    return redirect('dashboard:trc')

    else:
        form = DepositForm(instance=user)

    context = {
        'form': form,
        'plans': plans,
    }
    return render(request, 'dashboard/deposit.html', context)


@login_required(login_url='account:login')
def deposit_btc(request):
    user = request.user
    plan = Subscription.objects.filter(user=user, sub_currency="Btc").last()
    site = Site.objects.all()
    btc = ''

    for i in site:
        btc = i.btc

    # Custom QR Code Config
    logo = Image.open('static/img/icons/btcc.png')
    basewidth = 100
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(btc)
    QRcode.make()
    QRcolor = 'Green'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color='white').convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    qr = QRimg.save('static/img/qrcode/btc.png')

    context = {'plan': plan, 'qr': qr, 'btc': btc}
    return render(request, 'dashboard/deposit/btc.html', context)


@login_required(login_url='account:login')
def deposit_eth(request):
    user = request.user
    plan = Subscription.objects.filter(user=user, sub_currency="Eth").last()
    eth = ''

    for i in Site.objects.all():
        eth = i.eth

    # Custom QR Code Config
    logo = Image.open('static/img/icons/ethh.png')
    basewidth = 100
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(eth)
    QRcode.make()
    QRcolor = 'Green'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color='white').convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    qr = QRimg.save('static/img/qrcode/eth.png')

    context = {'plan': plan, 'qr': qr, 'eth': eth}
    return render(request, 'dashboard/deposit/eth.html', context)


@login_required(login_url='account:login')
def deposit_trc(request):
    user = request.user
    plan = Subscription.objects.filter(user=user, sub_currency="Trc20").last()
    usdt = ''

    for i in Site.objects.all():
        usdt = i.usdt

    # Custom QR Code Config
    logo = Image.open('static/img/icons/usdt.jpeg')
    basewidth = 100
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(usdt)
    QRcode.make()
    QRcolor = 'Green'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color='white').convert('RGB')
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    qr = QRimg.save('static/img/qrcode/usdt.png')

    context = {'plan': plan, 'qr': qr, 'usdt': usdt}
    return render(request, 'dashboard/deposit/trc.html', context)


@login_required(login_url='account:login')
def withdraw(request):
    user = request.user
    withdraw = Withdrawal(user=user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST, instance=withdraw, user=user)

        if form.is_valid():
            form.save()
            amount = form.cleaned_data['amount']
            wallet = form.cleaned_data['wallet']
            name = user.username
            # TODO: SEND CONFIRMATION MAIL TO USER
            context = ({
                'user': name,
                'amount': amount,
                'wallet': wallet.type,
                'address': wallet.address
            })
            html_version = './dashboard/mails/inactive_with.html'
            html_message = render_to_string(html_version, context)
            subject = 'siteName - Withdrawal Request'
            message = EmailMessage(subject, html_message,
                                   settings.EMAIL_HOST_USER, [user.email])
            message.content_subtype = 'html'
            message.send(fail_silently=True)
            # TODO: SEND CONFIRMATION MAIL TO ADMIN
            admin_msg = f'Hello Admin,\n\n{name.capitalize()} just initiated a withdrawal request.'
            admin_msg += f"\n\nKindly review the withdrawal request. And, if everything seems okay, "
            admin_msg += f"send the required amount to {name.capitalize()}'s specified address."
            admin_msg += f"\n\nAmount: ${amount}.00\nWallet type: {wallet.get_type_display()}\nWallet address: {wallet.address}"
            admin_msg += f"\n\nOnce that is done, confirm the transaction via the admin panel."
            admin_msg += f"\nTo do that, navigate to the Withdrawal table, click on the user and change the status from 'Pending' to 'Confirmed'."
            admin_msg += f'\n\nRegards,\nDevTeam.'
            message1 = EmailMessage(
                subject=f"User Withdrawal Notification",
                body=admin_msg,
                from_email='settings.EMAIL_HOST_USER',
                to=['okonkwogodspower@yahoo.com'],
            )
            message1.send(fail_silently=True)
            messages.success(
                request, ("Your withdrawal request was successful. Awaiting confirmation."))
            return redirect('dashboard:tot_withdraw')
    else:
        form = WithdrawalForm(user=user)

    context = {
        'form': form
    }
    return render(request, 'dashboard/withdraw.html', context)


@login_required(login_url='account:login')
def transfer(request):
    user = request.user
    transfer = Transfer(user=user)

    if request.method == 'POST':
        form = TransferForm(request.POST, instance=transfer)

        if form.is_valid():
            username = form.cleaned_data['username']
            amount = str(form.cleaned_data['amount'])
            request.session['transfer'] = {
                'username': username, 'amount': amount}
            return redirect('dashboard:confirm_transfer')

    else:
        form = TransferForm(instance=transfer)

    context = {
        'form': form
    }
    return render(request, 'dashboard/transfer.html', context)


@login_required(login_url='account:login')
def confirm_transfer(request):
    error = False
    sender = request.user

    tf_details = request.session.get('transfer', None)
    amount = Decimal(tf_details['amount'])
    username = tf_details['username']

    receiver = get_object_or_404(UserModel, username__iexact=username)
    if receiver is None:
        return redirect('dashboard:transfer')

    if request.method == 'POST':
        password = request.POST.get('password')

        match_password = check_password(password, sender.password)
        if not match_password:
            error = True
        else:
            new_tf = Transfer.objects.create(
                user=sender, username=receiver, amount=amount)
            request.session.pop('transfer')

            name = sender.username
            # TODO: SEND CONFIRMATION MAIL TO USER
            context = ({
                'user': name,
                'amount': new_tf.amount,
                'receiver': new_tf.username,
            })

            html_version = './dashboard/mails/inactive_tf.html'
            html_message = render_to_string(html_version, context)
            subject = 'siteName - Transfer Request'
            message = EmailMessage(subject, html_message,
                                   settings.EMAIL_HOST_USER, [sender.email])
            message.content_subtype = 'html'
            message.send(fail_silently=True)
            # TODO: SEND CONFIRMATION MAIL TO ADMIN
            admin_msg = f'Hello Admin,\n\n{name.capitalize()} just initiated a new transfer request.'
            admin_msg += f"\n\nKindly review the transfer request. And, if everything seems okay, "
            admin_msg += f"confirm the transaction via the admin panel."
            admin_msg += f"\nTo do that, navigate to the Transfer table, click on the user and change the status from 'Pending' to 'Confirmed'."
            admin_msg += f'\n\nRegards,\nDevTeam.'
            message1 = EmailMessage(
                subject=f"User Transfer Notification",
                body=admin_msg,
                from_email='settings.EMAIL_HOST_USER',
                to=['okonkwogodspower@yahoo.com'],
            )
            message1.send(fail_silently=True)

            messages.success(
                request, 'Your transfer request was successful. Awaiting confirmation.')
            return redirect('dashboard:tot_transfer')

    return render(request, 'dashboard/approve_transfer.html', {'error': error})


@login_required(login_url='account:login')
def wallet(request):
    user = request.user
    wallet = Wallet(user=user)
    object_list = Wallet.objects.filter(user=user)

    # Paginator
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')

    try:
        ref = paginator.page(page)
    except PageNotAnInteger:
        ref = paginator.page(1)
    except EmptyPage:
        ref = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        if 'add' in request.POST:
            form = WalletForm(request.POST, instance=wallet)
            if form.is_valid():
                form.save()
                messages.success(
                    request, ("New wallet address successfully added."))
                return redirect("dashboard:wallet")

    else:
        form = WalletForm(instance=wallet)

    context = {
        'form': form,
        'ref': ref,
    }
    return render(request, 'dashboard/wallet.html', context)


@login_required(login_url='account:login')
def del_wallet(request, pk):
    wallet = get_object_or_404(Wallet, id=pk)
    wallet.delete()
    return redirect("dashboard:wallet")


@login_required(login_url='account:login')
def tot_deposit(request):
    user = request.user
    object_list = Subscription.objects.filter(
        user=user).order_by('-initiated_on')

    # Paginator
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    print([i.type for i in object_list])

    try:
        sub = paginator.page(page)
    except PageNotAnInteger:
        sub = paginator.page(1)
    except EmptyPage:
        sub = paginator.page(paginator.num_pages)

    context = {
        'sub': sub,
        'page': page
    }
    return render(request, 'dashboard/tot_deposit.html', context)


@login_required(login_url='account:login')
def tot_withdraw(request):
    user = request.user
    object_list = Withdrawal.objects.filter(
        user=user).order_by('-initiated_on')

    # Paginator
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')

    try:
        withdraw = paginator.page(page)
    except PageNotAnInteger:
        withdraw = paginator.page(1)
    except EmptyPage:
        withdraw = paginator.page(paginator.num_pages)

    context = {
        'withdraw': withdraw,
        'page': page
    }
    return render(request, 'dashboard/tot_withdraw.html', context)


@login_required(login_url='account:login')
def tot_transfer(request):
    user = request.user
    object_list = Transfer.objects.filter(user=user).order_by('-initiated_on')

    # Pagination
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')

    try:
        transfer = paginator.page(page)
    except PageNotAnInteger:
        transfer = paginator.page(1)
    except EmptyPage:
        transfer = paginator.page(paginator.num_pages)

    context = {
        'transfer': transfer,
        'page': page
    }
    return render(request, 'dashboard/tot_transfer.html', context)


@login_required(login_url='account:login')
def my_referrals(request):
    referral = get_object_or_404(Referral, user=request.user)
    object_list = referral.get_recommend_profiles()

    # Paginator
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')

    try:
        total_recs = paginator.page(page)
    except PageNotAnInteger:
        total_recs = paginator.page(1)
    except EmptyPage:
        total_recs = paginator.page(paginator.num_pages)

    context = {
        'referrals': total_recs,
        'page': page
    }
    return render(request, 'dashboard/referral.html', context)


@login_required(login_url='account:login')
def logout_request(request):
    logout(request)
    # messages.info(request, 'You have successfully logged out')
    return redirect('account:login')
