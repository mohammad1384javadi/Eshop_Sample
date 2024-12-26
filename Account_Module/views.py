from django.contrib.auth import login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from .models import User
from utils.email_service import send_email


# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'Account_Module/register.html', {
            'register_form': register_form
        })

    def post(self, request: HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'نام کاربری با این ایمیل از قبل وجود دارد')
            else:
                user_password = register_form.cleaned_data.get('password')
                new_user = User(
                    email=user_email,
                    is_active=False,
                    username=user_email,
                    email_active_code=get_random_string(72)
                )
                new_user.set_password(user_password)
                new_user.save()
                try:
                    send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'Emails/active_account.html')
                except:
                    register_form.add_error('email', 'مشکلی در ارسال ایمیل وجود دارد')
                # return redirect(reverse('login_page'))

        return render(request, 'Account_Module/register.html', {
            'register_form': register_form
        })


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: show succes message to user
                return redirect(reverse('login_page'))
            else:
                # todo: show your account was activated message
                pass

        return Http404


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'Account_Module/login.html', {
            'login_form': login_form
        })

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری فعال نمی باشد')
                else:
                    user_password = login_form.cleaned_data.get('password')
                    is_pass_correct = user.check_password(user_password)
                    if not is_pass_correct:
                        login_form.add_error('email', 'حساب کاربری یا رمز عبور نادرست میباشد')
                    else:
                        login(request, user)
                        return redirect(reverse('home-page'))
            else:
                login_form.add_error('email', 'حساب کاربری یا رمز عبور نادرست میباشد')

        return render(request, 'Account_Module/login.html', {
            'login_form': login_form
        })


class ForgetPasswordView(View):
    def get(self, request):
        forget_pass_form = ForgetPasswordForm()
        return render(request, 'Account_Module/forget_pass.html', {
            'forget_pass_form': forget_pass_form
        })

    def post(self, request):
        forget_pass_form = ForgetPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('فراموشی کلمه عبور', user.email, {'user': user}, 'Emails/forget_password.html')
                redirect(reverse('login_page'))

        return render(request, 'Account_Module/forget_pass.html', {
            'forget_pass_form': forget_pass_form
        })


class ResetPasswordView(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is not None:
            reset_pass_form = ResetPasswordForm()
            return render(request, 'Account_Module/reset_pass.html', {
                'reset_pass_form': reset_pass_form,
                'user': user
            })
        else:
            return redirect(reverse('login_page'))

    def post(self, request, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        if reset_pass_form.is_valid():
            user: User = User.objects.filter(email_active_code__iexact=active_code).first()
            if user is None:
                redirect(reverse('login_page'))
            else:
                user_new_pass = reset_pass_form.cleaned_data.get('password')
                user.set_password(user_new_pass)
                user.email_active_code = get_random_string(72)
                user.is_active = True 
                user.save()
                return redirect(reverse('login_page'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home-page'))
