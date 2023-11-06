import random
import re

from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from .models import Account
from django.db.models import Q
from django.contrib import messages

from crypt_tools.hash.sm3 import sm3

# Create your views here.

def login(request):
    if request.method == 'POST':
        print('login/login: into login page...')
        nore = request.POST['nore']
        password = request.POST['password']
        res = Account.objects.filter(Q(email=nore) | Q(name=nore)).first()
        if not res:
            messages.error(request, 'Account does not exist!')
            print("login/login: Account does not exist")
        elif (nore == res.name or nore == res.email) and hex(sm3(password)) == res.password:
            print('login/login: log in successfully')
            print('login/login: username is ' + f'{res.name}')
            return render(request, './room/index.html', {
                'user_name': res.name,
            })
        else:
            messages.error(request, 'Wrong password!')
            print('login/login: wrong password')

    return render(request, './login/log_in.html')

def signup(request):
    if request.method == 'POST':
        print('signup/signup: into signup page...')
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_cf = request.POST['password_cf']
        res_name = Account.objects.filter(name=name).count()
        res_email = Account.objects.filter(email=email).count()
        if len(name) >= 10:
            print('signup/signup: name too long')
            messages.error(request, 'Your username is too long! please make sure it is shorter than 10 en characters.')
        elif res_name:
            print('signup/signup: duplicate name')
            messages.error(request, 'Your username has been registered! please re-enter a username.')
        elif res_email:
            print('signup/signup: duplicate email')
            messages.error(request, 'Your email has been registered! please re-enter an email.')
        elif not valid_email(email):
            print('signup/signup: email not valid')
            messages.error(request, 'Your email is not valid!')
        elif len(password) >= 20:
            print('signup/signup: password too long')
            messages.error(request, 'Your password is too long! please make sure it is shorter than 20 en characters.')
        elif len(password) <= 5:
            print('signup/signup: password too short')
            messages.error(request, 'Your password is too short! please make sure it is longer than 20 en characters.')
        elif password != password_cf:
            print('signup/signup: two password are not same')
            messages.error(request, 'The two password are not same! please check them again.')
        else:
            Account.objects.create(name=name, email=email, password=hex(sm3(password)))
            print('signup/signup: register account successfully')
            messages.success(request, 'Register account successfully.')
            return render(request, './login/log_in.html')

    return render(request, './login/sign_up.html')

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
def valid_email(email: str) -> bool:
    if re.fullmatch(regex, email):
        return True
    return False

def forget(request):
    if request.method == 'POST':
        print('forget/forget: into forget page...')
        verify = request.POST['verify']
        verify_ = request.session['msg']['code']
        email = request.session['msg']['email']
        password = request.POST['password']
        password_cf = request.POST['password_cf']
        if verify_ != verify:
            print('forget/forget: invalid verificaition code')
            messages.error(request, 'The verification code is not valid!')
        elif len(password) >= 20:
            print('forget/forget: password too long')
            messages.error(request, 'Your password is too long! please make sure it is shorter than 20 en characters.')
        elif len(password) <= 5:
            print('forget/forget: password too short')
            messages.error(request, 'Your password is too short! please make sure it is longer than 20 en characters.')
        elif password != password_cf:
            print('forget/forget: two password are not same')
            messages.error(request, 'The two password are not same! please check them again.')
        else:
            acnt = Account.objects.filter(email=email).first()
            acnt.password = hex(sm3(password))
            acnt.save()
            print('forget/forget: password reset complete')
            messages.success(request, 'Password reset complete!')
            request.session['msg'] = {}
            return render(request, './login/log_in.html')
    return render(request, './login/forget.html')

host_email = "2951335562@qq.com"
def send_vericode(request):
    if request.method == 'POST':
        print('send_ver/send_ver: ready to send...')
        nore = request.POST['nore']
        email = ''
        if Account.objects.filter(email=nore).count():
            email = nore
        elif Account.objects.filter(name=nore).count():
            email = Account.objects.filter(name=nore).first().email
        if not email:
            print('send_ver/send_ver: name or email has not been registered')
            messages.error(request, 'The name or email has not been registered!')
        else:
            code = random_str()
            request.session['msg'] = { 'code': code, 'email': email }
            msg = "Your secret verification code is " + code + ", only valid in 5 min."
            send_mail("Welcome to SecretChat", msg, host_email, [email], fail_silently=False)
            print('send_ver/send_ver: verification code has been sent')
            messages.success(request, 'The verification code has been sent.')
    return render(request, './login/forget.html')

def random_str():
    _str = '1234567890abcdefghijklmnopqestuvwxyz'
    return ''.join(random.choice(_str) for _ in range(4))

def index(request):
    print('into index...')
    return redirect(reverse('login'))
