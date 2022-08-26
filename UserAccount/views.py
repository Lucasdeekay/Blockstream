import random
import string

from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from UserAccount.forms import RegistrationForm, LoginForm, ForgotPasswordForm, PasswordRetrievalForm, \
    UpdatePasswordForm, AmountForm, TextForm
from UserAccount.models import Clientele, Password, Referral, Account, Deposit, Investment, Withdrawal

# Create your views here.
from mysite.settings import EMAIL_HOST_USER


# Custom functions

# Function checks the password correction made by the user
def check_password(password, confirm_password):
    if password != confirm_password:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:regsiter'))


# Function checks the amount range of the plans for investment
def check_investment_plan_range(request, plan, amount):
    # Check if amount is not out of plan range
    if (plan == 'Basic' and (amount < 100 or amount > 499)) or (plan == 'Silver' and (amount < 500 or amount > 999)) \
            or (plan == 'Gold' and (amount < 1000 or amount > 4999)) \
            or (plan == 'Platinum' and amount < 10000):
        # Display an error message
        messages.error(request, 'Amount is either below or above plan range')
        # Redirect back to investment page
        return HttpResponseRedirect(reverse("UserAccount:invest"))


# Function checks if investments have expired
def check_investment_expiry():
    all_inv = Investment.objects.all()
    for i in all_inv:
        i.expiry()


# Check if amount is out of withdrawal range
def check_withdrawal_range(request, amount):
    # Check if amount is not out of range
    if amount < 100 or amount > 500000:
        # Display an error message
        messages.error(request, 'Amount is either below or above withdrawal range')
        # Redirect back to investment page
        return HttpResponseRedirect(reverse("UserAccount:withdraw"))


# View displays the login page and authenticates user login
def log_in(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Redirect to the dashboard
        return HttpResponseRedirect(reverse('UserAccount:dashboard'))
    # If user is not logged in
    else:
        # Check if form was submitted
        if request.method == 'POST':
            # get form
            form = LoginForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Get form data
                username = form.cleaned_data.get('username').strip()
                password = form.cleaned_data.get('password').strip()
                # Authenticate the login details
                user = authenticate(request, username=username, password=password)

                # Check if user is available
                if user is not None:
                    # Login the user
                    login(request, user)

                    # Send message
                    messages.success(request, "Login successful")
                    # Redirect to the dashboard page
                    return HttpResponseRedirect(reverse('UserAccount:dashboard'))
                # If user is not available
                else:
                    # Send message
                    messages.error(request, "Invalid login details")
                    # Redirect to the login page
                    return HttpResponseRedirect(reverse('UserAccount:login'))
        # If form was not submitted
        else:
            # Get form
            form = LoginForm()
        # Render the login display with form
        return render(request, 'useraccount/login.html', {'form': form})


# View displays the forgot password page and processes the data submitted
def forgotten_password(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Redirect to the dashboard
        return HttpResponseRedirect(reverse('UserAccount:dashboard'))
    # If user is not logged in
    else:
        # Check if form was submitted
        if request.method == 'POST':
            # get form
            form = ForgotPasswordForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Get form data
                username = form.cleaned_data['username'].strip()
                email = form.cleaned_data['email'].strip()
                # Get all users
                all_user = User.objects.all()
                # Loop
                for user in all_user:
                    # Check if user exists
                    if user.username == username and user.email == email:
                        # Get clientele
                        clientele = Clientele.objects.get(user=user)
                        # Generate password
                        recovery_password = ''.join(
                            [random.choice(string.ascii_letters + string.digits) for i in range(12)])

                        # Get all active recovery password passwords
                        all_passwords = Password.objects.filter(is_active=True)
                        # Loop
                        for password in all_passwords:
                            # Check if clientele has an unused active recovery password
                            if password.clientele == clientele and password.is_active:
                                # Make the unused password inactive
                                password.is_active = False
                                # Break the loop
                                break

                        # Create recovery password object
                        Password.objects.create(clientele=clientele, recovery_password=recovery_password,
                                                time=timezone.now())

                        # Create and send mail to the clientele
                        subject = 'Password Recovery'
                        msg = f"Recovery password will expire after an hour. Your password is displayed below"
                        context = {'subject': subject, 'msg': msg, 'recovery_password': recovery_password,
                                   'clientele': clientele}
                        html_message = render_to_string('useraccount/msg.html', context=context)

                        send_mail(subject, msg, EMAIL_HOST_USER, [email], html_message=html_message,
                                  fail_silently=False)
                        # Display message
                        messages.success(request, "Recovery password has been successfully sent")
                        # Redirect to password retrieval page
                        return HttpResponseRedirect(reverse('UserAccount:password_retrieval', args=(clientele.id,)))
                # If user is not found by the end of the loop
                else:
                    # Display message
                    messages.error(request, "User profile not found")
                    # Redirect to forgot password page
                    return HttpResponseRedirect(reverse('UserAccount:forgot_password'))
        # Check if form was not submitted
        else:
            # Get form
            form = ForgotPasswordForm()
        # Render forgot password page
        return render(request, 'useraccount/forgot_password.html', {'form': form})


# View displays the password retrieval page and processes the data submitted
def password_retrieval(request, clientele_id):
    all_passwords = Password.objects.filter(is_active=True)
    for password in all_passwords:
        password.expiry()
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Redirect to the dashboard
        return HttpResponseRedirect(reverse('UserAccount:dashboard'))
    # If user is not logged in
    else:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, id=clientele_id)
        # Check if form was submitted
        if request.method == 'POST':
            # Get form
            form = PasswordRetrievalForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                password = form.cleaned_data['password'].strip()
                all_password = Password.objects.all()
                clientele = get_object_or_404(Clientele, id=clientele_id)

                for passcode in all_password:
                    if passcode.clientele == clientele and passcode.recovery_password == password and passcode.is_active:
                        subject = 'Password Recovery Successful'
                        msg = "Account has been successfully recovered. Kindly proceed to update your password"
                        context = {'subject': subject, 'msg': msg, 'clientele':clientele}
                        html_message = render_to_string('useraccount/msg.html', context=context)

                        send_mail(subject, msg, EMAIL_HOST_USER, [clientele.email], html_message=html_message,
                                  fail_silently=False)

                        messages.success(request,
                                         'Account has been successfully recovered. Kindly update your password')
                        return HttpResponseRedirect(reverse('UserAccount:update_password', args=(clientele_id,)))
                else:
                    messages.error(request,
                                   "Incorrect recovery password. Click on resend to get the retrieval password again")
                    return HttpResponseRedirect(reverse('UserAccount:password_retrieval', args=(clientele_id,)))
        # If form was not submitted
        else:
            # Get form
            form = PasswordRetrievalForm()
        # Create context
        context = {'current_clientele': current_clientele, 'clientele_id': clientele_id, 'form': form}
        # Render password retrieval page
        return render(request, 'useraccount/password_retrieval.html', context)


# View displays the resend password page and processes the data submitted
def resend_password(request, clientele_id):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Redirect to the dashboard
        return HttpResponseRedirect(reverse('UserAccount:dashboard'))
    # If user is not logged in
    else:
        # Get current clientele
        clientele = Clientele.objects.get(id=clientele_id)
        # Generate password
        recovery_password = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(12)])

        # Get all active recovery password passwords
        all_passwords = Password.objects.filter(is_active=True)
        # Loop
        for password in all_passwords:
            # Check if clientele has an unused active recovery password
            if password.clientele == clientele and password.is_active:
                # Make the unused password inactive
                password.is_active = False
                # Break the loop
                break

        # Create recovery password object
        Password.objects.create(clientele=clientele, recovery_password=recovery_password,
                                time=timezone.now())

        # Create and send mail to the clientele
        subject = 'Password Recovery'
        msg = f"Recovery password will expire after an hour. Your password is displayed below"
        context = {'subject': subject, 'msg': msg, 'recovery_password': recovery_password, 'clientele': clientele}
        html_message = render_to_string('useraccount/msg.html', context=context)

        send_mail(subject, msg, EMAIL_HOST_USER, [clientele.email], html_message=html_message,
                  fail_silently=False)

        # Display message
        messages.success(request, "Recovery password has been successfully sent")
        # Redirect to password retrieval page
        return HttpResponseRedirect(reverse('UserAccount:password_retrieval', args=(clientele.id,)))


# View displays the update password page and processes the data submitted
def update_password(request, clientele_id):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Redirect to the dashboard
        return HttpResponseRedirect(reverse('UserAccount:dashboard'))
    # If user is not logged in
    else:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, id=clientele_id)
        # Check if form was submitted
        if request.method == 'POST':
            # Get form
            form = UpdatePasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password'].strip()
                password2 = form.cleaned_data['confirm_password'].strip()

                if password1 == password2:
                    user = Clientele.objects.get(id=clientele_id).user
                    user.set_password(password1)
                    user.save()

                    subject = 'Password Update Successful'
                    msg = "Account password has  been successfully changed"
                    context = {'subject': subject, 'msg': msg}
                    html_message = render_to_string('useraccount/msg.html', context=context)

                    send_mail(subject, msg, EMAIL_HOST_USER, [user.email], html_message=html_message,
                              fail_silently=False)

                    messages.success(request, 'Password successfully changed')
                    return HttpResponseRedirect(reverse('UserAccount:login'))
                else:
                    messages.error(request, "Password does not match")
                    return HttpResponseRedirect(reverse('UserAccount:update_password', args=(clientele_id,)))
        # If form was not submitted
        else:
            # Get form
            form = UpdatePasswordForm()
        # Create context
        context = {'current_clientele': current_clientele, 'clientele_id': clientele_id, 'form': form}
        # Render password retrieval page
        return render(request, 'useraccount/update_password.html', context)


# View displays and authenticates user registration
def register(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Redirect to the user account's dashboard
        return HttpResponseRedirect(reverse('UserAccount:dashboard'))
    # If user is not logged in
    else:
        # Check if form has been submitted
        if request.method == 'POST':
            # Get form
            form = RegistrationForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Collect form data
                full_name = form.cleaned_data.get('full_name').capitalize().strip()
                username = form.cleaned_data.get('username').strip()
                phone_no = form.cleaned_data.get('phone_number').strip()
                email = form.cleaned_data.get('email').strip()
                password = form.cleaned_data.get('password').strip()
                confirm_password = form.cleaned_data.get('confirm_password').strip()
                referer = request.POST.get('referer').strip()

                # Check if passwords does not match
                check_password(password, confirm_password)

                # Get all registered clienteles
                all_clienteles = Clientele.objects.all()


                # Loop through all clienteles to check if user already exists
                for clientele in all_clienteles:
                    if username == clientele.user.username:
                        messages.error(request, "User ID already in use")
                        return HttpResponseRedirect(reverse('UserAccount:register'))
                    elif email == clientele.email:
                        messages.error(request, "Email already in use")
                        return HttpResponseRedirect(reverse('UserAccount:register'))
                # If user does not exist
                else:
                    # Create a new user
                    new_user = User.objects.create_user(username=username, email=email, password=password)
                    # Create a new clientele and link te new user to it
                    clientele = Clientele.objects.create(user=new_user, full_name=full_name, phone_no=phone_no, email=email)
                    # Create new account
                    Account.objects.create(clientele=clientele)
                    # Check if new user was referred
                    if referer != '':
                        # Get the referer
                        user_referred = get_object_or_404(User, username=referer)
                        user_referer = get_object_or_404(Clientele, user=user_referred)
                        # Create a new referer object
                        Referral.objects.create(user=new_user, referer=user_referer, date=timezone.now())

                    # Create a message to email to user upon successful registration
                    subject = 'Password Update Successful'
                    msg = "Registration successful. We look forward toa solid partnership with you at Blockstream. At "\
                          "Blockstream, we work towards building a world where everyone can succeed. Welcome to the " \
                          "Blockstream family."
                    context = {'subject': subject, 'msg': msg}
                    html_message = render_to_string('useraccount/msg.html', context=context)

                    # Send email
                    send_mail(subject, msg, EMAIL_HOST_USER, [email], html_message=html_message,
                              fail_silently=False)
                    # Notify user that email has been sent
                    messages.success(request,
                                     "Registration successful.")
                    # Redirect to login page
                    return HttpResponseRedirect(reverse('UserAccount:login'))
        # If form is not submitted
        else:
            # display form
            form = RegistrationForm()
        # Render registration page
        return render(request, 'useraccount/register.html', {'form': form})


# View displays and authenticates user registration
def ref_register(request, ref):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Redirect to the user account's dashboard
        return HttpResponseRedirect(reverse('UserAccount:dashboard'))
    # If user is not logged in
    else:
        # display form
        form = RegistrationForm()
        # Render registration page
        return render(request, 'useraccount/register.html', {'form': form, 'ref': ref})


# View logs out the user
def log_out(request):
    logout(request)
    # Redirect to login page
    return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the dashboard of the user
def dashboard(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Get current clientele's account
        account = get_object_or_404(Account, clientele=current_clientele)
        # Update account
        account.update()

        check_investment_expiry()
        # Create context
        context = {'account': account, 'clientele': current_clientele}
        # Render dashboard page
        return render(request, 'useraccount/dashboard.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the deposit page of the user
def deposit(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Check if form was submitted
        if request.method == 'POST':
            # Get form
            form = AmountForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Get form data
                amount = form.cleaned_data.get('amount')
                mode = 'USDT' if request.POST.get('mode') == 'usdt' else 'BTC'

                # Generate transaction id
                transaction_id = ''.join(
                    [random.choice(string.ascii_letters + string.digits) for i in range(8)])
                # Create new deposit
                Deposit.objects.create(clientele=current_clientele, mode=mode, amount=amount,
                                       transaction_id=transaction_id, date=timezone.now())

                # Create and send mail to the clientele
                subject = 'New Deposit Notice'
                msg = f"Transaction ID for the proposed deposit of ${amount} in {mode} is displayed below"
                context = {'subject': subject, 'msg': msg, 'recovery_password': transaction_id,
                           'clientele': current_clientele}
                html_message = render_to_string('useraccount/msg.html', context=context)

                send_mail(subject, msg, EMAIL_HOST_USER, [current_clientele.email], html_message=html_message,
                          fail_silently=False)
                # Display message
                messages.success(request, "Transaction ID has been successfully sent to your email")

                # Redirect to wallet page
                return HttpResponseRedirect(reverse('UserAccount:wallet', args=(mode,)))
        # If form was not submitted
        else:
            # Get form
            form = AmountForm()
        # Create context
        context = {'form': form, 'clientele': current_clientele}
        # Render deposit page
        return render(request, 'useraccount/deposit.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the confirm deposit page and verified deposit's transaction id
def confirm_deposit(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Check if form was submitted
        if request.method == 'POST':
            # Get otp input from user
            transaction_id = request.POST.get("transaction_id").strip()
            try:
                deposit = Deposit.objects.get(clientele=current_clientele, transaction_id=transaction_id)
                deposit.tid_confirmed = True
                deposit.save()
                messages.success(request, "Deposit confirmation received. Account balance will be updated after it has been validated")
                # Redirect to dashboard page
                return HttpResponseRedirect(reverse('UserAccount:dashboard'))
            except Exception:
                messages.success(request, "Deposit record does not exist")
                # Redirect to withdraw page
                return HttpResponseRedirect(reverse('UserAccount:confirm_deposit'))

        # Create context
        context = {'clientele': current_clientele}
        # Render investment page
        return render(request, 'useraccount/confirm_deposit.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the wallet page of the user
def wallet(request, mode):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Instantiate btc wallet
        account = 'btckllkjkkjojlk'
        # If mode is usdt
        if mode == 'USDT':
            # Instantiate usdt wallet
            account = 'usdtbbjjhkjkhk'

        # Create context
        context = {'currency': mode.upper(), 'account': account, 'clientele': current_clientele}
        # Render the wallet page
        return render(request, 'useraccount/wallets.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the investment page of the user
def invest(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        check_investment_expiry()
        # Check if form was submitted
        if request.method == 'POST':
            # Get form
            form = AmountForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Get form data
                amount = form.cleaned_data['amount']
                plan = request.POST.get('plan')

                # Check if amount is out of investment plan range
                check_investment_plan_range(request, plan, amount)

                # Get user account
                account = get_object_or_404(Account, clientele=current_clientele)
                # Check if account balance is less than amount needed for investment
                if account.balance < amount:
                    # Send message
                    messages.error(request, "Investment unsuccessful. Insufficient current balance")
                    # Redirect to investment page
                    return HttpResponseRedirect(reverse('UserAccount:invest'))
                else:
                    # Create a new Investment instance
                    Investment.objects.create(clientele=current_clientele, amount=amount, plan=plan, date=timezone.now(), is_active=True)
                    # update account
                    account.balance -= amount
                    account.active_investments += 1
                    account.total_investments += 1
                    account.save()
                    # Redirect to dashboard page
                    return HttpResponseRedirect(reverse('UserAccount:dashboard'))

        # If form was not submitted
        else:
            # Get form
            form = AmountForm()
        # Create context
        context = {'form': form, 'clientele': current_clientele}
        # Render investment page
        return render(request, 'useraccount/invest.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the withdrawal page of the user
def withdraw(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Check if form was submitted
        if request.method == 'POST':
            # Get form
            form = AmountForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Get form data
                amount = form.cleaned_data['amount']
                mode = request.POST.get('mode')

                # Check if amount is out of withdrawal range
                check_withdrawal_range(request, amount)

                # Get user account
                account = get_object_or_404(Account, clientele=current_clientele)
                # Check if account balance is less than amount needed for investment
                if account.balance < amount:
                    # Send message
                    messages.error(request, "Withdrawal unsuccessful. Insufficient current balance")
                    # Redirect to investment page
                    return HttpResponseRedirect(reverse('UserAccount:invest'))

                else:
                    # Generate otp
                    otp = ''.join(
                        [random.choice(string.ascii_letters + string.digits) for i in range(6)])
                    # Create a new Withdrawal instance
                    Withdrawal.objects.create(clientele=current_clientele, mode=mode, amount=amount,
                                              otp=otp, date=timezone.now())

                    # Create and send mail to the clientele
                    subject = 'New Withdrawal Request'
                    msg = f"OTP for the proposed deposit of ${amount} in {mode} is displayed below"
                    context = {'subject': subject, 'msg': msg, 'recovery_password': otp,
                               'clientele': current_clientele}
                    html_message = render_to_string('useraccount/msg.html', context=context)

                    send_mail(subject, msg, EMAIL_HOST_USER, [current_clientele.email], html_message=html_message,
                              fail_silently=False)
                    # Display message
                    messages.success(request, "OTP has been successfully sent to your email")
                    # Redirect to dashboard page
                    return HttpResponseRedirect(reverse('UserAccount:confirm_withdrawal'))

        # If form was not submitted
        else:
            # Get form
            form = AmountForm()
        # Create context
        context = {'form': form, 'clientele': current_clientele}
        # Render investment page
        return render(request, 'useraccount/withdraw.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the confirm withdrawal page and verified withdrawal otp
def confirm_withdrawal(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Check if form was submitted
        if request.method == 'POST':
            # Get otp input from user
            otp = request.POST.get("otp").strip()
            wallet_addr = request.POST.get("wallet").strip()
            try:
                withdrawal = Withdrawal.objects.get(clientele=current_clientele, otp=otp)
                withdrawal.otp_confirmed = True
                withdrawal.wallet = wallet_addr
                withdrawal.save()
                messages.success(request, "Withdrawal will be sent into your wallet after it has been validated")
                # Redirect to dashboard page
                return HttpResponseRedirect(reverse('UserAccount:dashboard'))
            except Exception:
                messages.error(request, "Withdrawal request cancelled due to invalid OTP. Try again!")
                # Redirect to withdraw page
                return HttpResponseRedirect(reverse('UserAccount:withdraw'))

        # Create context
        context = {'clientele': current_clientele}
        # Render investment page
        return render(request, 'useraccount/confirm_withdrawal.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the profits page of the user
def profit_record(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Get current clientele profits
        investment = Investment.objects.filter(clientele=current_clientele, is_active=True).order_by('-date')
        investment_paginator = Paginator(investment, 10)  # Show 10 withdrawals per page.
        investment_page_number = request.GET.get('page')  # Get each paginated pages
        investment_obj = investment_paginator.get_page(investment_page_number)  # Insert the number of items into page
        # Create context
        context = {
            'investment': investment,
            'investment_obj': investment_obj,
            'clientele': current_clientele
        }
        # Render profits page
        return render(request, 'useraccount/profit_record.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the transaction page of the user
def transaction(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:

        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)

        # Get current clientele deposits
        deposit = Deposit.objects.filter(clientele=current_clientele).order_by('-date')
        deposit_paginator = Paginator(deposit, 10)  # Show 10 deposits per page.
        deposit_page_number = request.GET.get('page')  # Get each paginated pages
        deposit_obj = deposit_paginator.get_page(deposit_page_number)  # Insert the number of items into page

        # Get current clientele withdrawals
        withdrawal = Withdrawal.objects.filter(clientele=current_clientele).order_by('-date')
        withdrawal_paginator = Paginator(withdrawal, 10)  # Show 10 withdrawals per page.
        withdrawal_page_number = request.GET.get('page')  # Get each paginated pages
        withdrawal_obj = withdrawal_paginator.get_page(withdrawal_page_number)  # Insert the number of items into page

        # Get current clientele referrals
        referral = Referral.objects.filter(user=request.user).order_by('-date')
        referral_paginator = Paginator(referral, 10)  # Show 10 referral per page.
        referral_page_number = request.GET.get('page')  # Get each paginated pages
        referral_obj = referral_paginator.get_page(referral_page_number)  # Insert the number of items into page


        # Create context
        context = {
            'clientele': current_clientele,
            'deposit': deposit,
            'deposit_obj': deposit_obj,
            'withdrawal': withdrawal,
            'withdrawal_obj': withdrawal_obj,
            'referral': referral,
            'referral_obj': referral_obj
        }
        # Render transaction page
        return render(request, 'useraccount/transaction.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the referral page of the user
def refer(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)

        # Get current clientele referer
        try:
            referer = get_object_or_404(Referral, user=request.user)
        except Exception:
            referer= None

        # Get current clientele referrals
        try:
            referral = Referral.objects.filter(referer=current_clientele).order_by('-date')
            referral_paginator = Paginator(referral, 10)  # Show 10 referral per page.
            referral_page_number = request.GET.get('page')  # Get each paginated pages
            referral_obj = referral_paginator.get_page(referral_page_number)  # Insert the number of items into page
        except Exception:
            referral = None
            referral_obj = None

        # Create context
        context = {
            'clientele': current_clientele,
            'referer': referer,
            'referral': referral,
            'referral_obj': referral_obj
        }
        # Render referral page
        return render(request, 'useraccount/refer.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the support page of the user
def support(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Check if form was submitted
        if request.method == 'POST':
            # Get form
            form = TextForm(request.POST)
            # Check if form is valid
            if form.is_valid():
                # Get form data
                message = form.cleaned_data['message'].strip()
                # Create a message to email to user upon successful registration
                subject = 'Support Ticket'
                msg = f'''
from: {current_clientele}
email: {current_clientele.email}


{message}
'''
                context = {'subject': subject, 'msg': msg, 'clientele': "Admin"}
                html_message = render_to_string('useraccount/msg.html', context=context)

                # Send email
                send_mail(subject, msg, EMAIL_HOST_USER, [EMAIL_HOST_USER], html_message=html_message)
                # Display message
                messages.success(request, "Message successfully sent")

        # If form was not submitted
        else:
            # Get form
            form = TextForm()
        # Create context
        context = {'clientele': current_clientele, 'form': form}
        # Render support page
        return render(request, 'useraccount/support.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the settings page of the user
def settings(request):
    # Check if user is logged in and not a super user
    if request.user.is_authenticated and not request.user.is_superuser:
        # Get current clientele
        current_clientele = get_object_or_404(Clientele, user=request.user)
        # Get submit data
        submit = request.POST.get('submit')
        # Check if password form is submitted
        if submit == 'updateProfile':
            # Get form data
            full_name = request.POST.get('full_name').capitalize().strip()
            phone_no = request.POST.get('phone_no').strip()
            email = request.POST.get('email').strip()

            # Modify clientele details
            current_clientele.full_name, current_clientele.phone_no, current_clientele.email = full_name, phone_no, email
            current_clientele.save()

            messages.success(request, " Profile successfully updated")
            # Redirect to login page
            return HttpResponseRedirect(reverse('UserAccount:settings'))
        # Check if profile form was submitted
        elif submit == 'updatePassword':
            if request.method == 'POST':
                # Get form
                form = UpdatePasswordForm(request.POST)
                # Check if form is valid
                if form.is_valid():
                    # Get form data
                    password1 = form.cleaned_data['password'].strip()
                    password2 = form.cleaned_data['confirm_password'].strip()
                    # Check if password match
                    if password1 == password2:
                        # Set password for current user
                        request.user.set_password(password1)
                        request.user.save()
                        # Display success message
                        messages.success(request, 'Password successfully changed. Kindly login with your new paasword')
                        # Redirect back to page
                        return HttpResponseRedirect(reverse('UserAccount:logout'))
                    # If password does not match
                    else:
                        # Display message
                        messages.error(request, "Password does not match")
                        # Redirect back to page
                        return HttpResponseRedirect(reverse('UserAccount:settings'))
            # If form is not submitted
            else:
                # Get form
                form = UpdatePasswordForm()
            # Create context
            context = {'clientele': current_clientele, 'form': form}
            # Render settings page
            return render(request, 'useraccount/settings.html', context)
        else:
            # Get form
            form = UpdatePasswordForm()
            # Create context
            context = {'clientele': current_clientele, 'form': form}
            # Render settings page
            return render(request, 'useraccount/settings.html', context)
    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View displays the admin page of the user
def admin_manager(request):
    # Check if user is logged in and not a super user
    if (request.user.is_authenticated and not request.user.is_superuser) and \
            (User.objects.filter(username=request.user.username, groups__name='Manager').exists()):
        check_investment_expiry()
        try:
            # Get all the deposits made and withdrawal requested
            deposits = Deposit.objects.filter(tid_confirmed=True, is_verified=False).order_by('-date')
            deposits_paginator = Paginator(deposits, 10)  # Show 10 deposits per page.
            deposits_page_number = request.GET.get('page')  # Get each paginated pages
            deposits_obj = deposits_paginator.get_page(deposits_page_number)  # Insert the number of items into page
        except Exception:
            deposits = None
            deposits_obj = None

        try:
            withdrawals = Withdrawal.objects.filter(otp_confirmed=True, is_verified=False).order_by('-date')
            withdrawals_paginator = Paginator(withdrawals, 10)  # Show 10 withdrawals per page.
            withdrawals_page_number = request.GET.get('page')  # Get each paginated pages
            withdrawals_obj = withdrawals_paginator.get_page(withdrawals_page_number)  # Insert the number of items into page
        except Exception:
            withdrawals = None
            withdrawals_obj = None

        try:
            active_investment = Investment.objects.filter(is_active=True).order_by('-date')
            active_investment_paginator = Paginator(active_investment, 10)  # Show 10 active investment per page.
            active_investment_page_number = request.GET.get('page')  # Get each paginated pages
            active_investment_obj = active_investment_paginator.get_page(active_investment_page_number)  # Insert the number of items into page
        except Exception:
            active_investment = None
            active_investment_obj = None

        # Create context
        context = {
            'deposits': deposits,
            'deposits_obj': deposits_obj,
            'withdrawals': withdrawals,
            'withdrawals_obj': withdrawals_obj,
            'investments': active_investment,
            'active_investment_obj': active_investment_obj,
        }
        # Render admin manager page
        return render(request, 'useraccount/admin_manager.html', context)

    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View approves the deposits and withdrawals the admin page of the user
def approve(request, mode, id):
    # Check if user is logged in and not a super user
    if (request.user.is_authenticated and not request.user.is_superuser) and \
            (User.objects.filter(username=request.user.username, groups__name='Manager').exists()):

        # Check the mode of data
        if mode == 'deposit':
            # Get specified deposit
            depo = get_object_or_404(Deposit, id=id)
            # Change verification status
            depo.is_verified = True
            depo.save()

            # Update Account balance
            account = Account.objects.get(clientele=depo.clientele)
            account.balance += depo.amount
            account.total_deposit += depo.amount
            account.save()

            try:
                # Get referer
                referer = get_object_or_404(Referral, referer=depo.clientele)
                # Add referer bonus
                referer.bonus += 0.02 * depo.amount
                referer.save()
            except Exception:
                pass

            # Get referer account
        # Otherwise
        else:
            # Get specified withdrawal
            withdrawal = get_object_or_404(Withdrawal, id=id)
            # Change verification status
            withdrawal.is_verified = True
            withdrawal.save()

            # Update Account balance
            account = Account.objects.get(clientele=withdrawal.clientele)
            account.save()

        # Render admin manager page
        return HttpResponseRedirect(reverse('SiteHome:admin_manager'))

    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View declines the deposits and withdrawals the admin page of the user
def decline(request, mode, id):
    # Check if user is logged in and not a super user
    if (request.user.is_authenticated and not request.user.is_superuser) and \
            (User.objects.filter(username=request.user.username, groups__name='Manager').exists()):

        # Check the mode of data
        if mode == 'deposit':
            # Get specified deposit
            deposit = get_object_or_404(Deposit, id=id)
            # Delete deposit information
            deposit.delete()
        # Otherwise
        else:
            # Get specified withdrawal
            withdrawal = get_object_or_404(Withdrawal, id=id)
            # Update Account balance
            account = Account.objects.get(clientele=withdrawal.clientele)
            account.total_withdrawal -= withdrawal.amount
            # Change withdrawal information
            withdrawal.delete()

        # Render admin manager page
        return HttpResponseRedirect(reverse('SiteHome:admin_manager'))

    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))


# View declines the deposits and withdrawals the admin page of the user
def update_profit(request, id):
    # Check if user is logged in and not a super user
    if (request.user.is_authenticated and not request.user.is_superuser) and \
            (User.objects.filter(username=request.user.username, groups__name='Manager').exists()):
        # Get profit
        amount = request.POST.get('amount')
        # Get investment
        investment = get_object_or_404(Investment, id=id)
        # Add profit
        investment.profit += float(amount)
        # Save investment
        investment.save()

        # Render admin manager page
        return HttpResponseRedirect(reverse('SiteHome:admin_manager'))

    # If user is not logged in
    else:
        # Redirect to login page
        return HttpResponseRedirect(reverse('UserAccount:login'))