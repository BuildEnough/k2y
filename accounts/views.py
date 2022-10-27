from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
# 회원가입 페이지 및 user 데이터 생성
def signup(request):
    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('review:index')
    else:
        signup_form = CustomUserCreationForm()

    context = {
        'signup_form': signup_form,
    }

    return render(request, 'accounts/signup.html', context)

# 회원 목록 조회 페이지
def index(request):
    users = get_user_model().objects.all()

    context = {
        'users': users,
    }

    return render(request, 'accounts/index.html', context)

# 회원 정보 조회 페이지
def detail(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)

    context = {
        'user': user,
    }

    return render(request, 'accounts/detail.html', context)

# 로그인
def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('review:index')
    else:
        login_form = AuthenticationForm()

    context = {
        'login_form': login_form,
    }

    return render(request, 'accounts/login.html', context)

# 로그아웃
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, '로그아웃했습니다.')
    return redirect('review:index')