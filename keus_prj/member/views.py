from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Member
from .forms import MemberForm, UpdateProfileForm


def join(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member_data = form.cleaned_data
            if member_data['password'] == member_data['PasswordOK']:
                user = Member.objects.create_user(
                    username=member_data['username'],
                    password=member_data['password'],
                    Tell=member_data['Tell'],
                    email=member_data['email']
                )
                return redirect(reverse('member:login'))
            else:
                form.add_error('PasswordOK', '비밀번호가 일치하지 않습니다.')
    else:
        form = MemberForm()

    return render(request, 'member/join.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(reverse('main:main'))
        else:
            return render(request, 'member/login.html', {'error_message': '아이디 또는 비밀번호를 잘못 입력했습니다.'})
    return render(request, 'member/login.html')

# 로그인 성공시 메인페이지로 이동(지금은 임시로 member/header.html 로 )
def header(request):
    return render(request, 'member/header.html')

@login_required  # 로그인이 필수적으로 요구되는 사항(logout,mypage)
def logout(request):
    auth_logout(request)
    return redirect(reverse('member:login'))

# 아이디 및 비밀번호 찾기를 위한 find 함수 생성
def find(request):
    if request.method == 'GET':
        find_type = request.GET.get('type')  # type은 아이디 찾기인지 비밀번호 찾기인지 구분하는 매개변수 -> HTML hidden 지정
        if find_type == 'username':
            email = request.GET.get('email', '')
            Tell = request.GET.get('Tell', '')

            try:
                member = Member.objects.get(email=email, Tell=Tell)
                return JsonResponse({'username': member.username})  # 아이디를 JSON 형태로 응답

            except ObjectDoesNotExist:
                return JsonResponse({'error': '사용자를 찾을 수 없습니다.'})  # 사용자를 찾지 못한 경우 에러 응답

        elif find_type == 'password':
            username = request.GET.get('username', '')
            email = request.GET.get('email', '')
            Tell = request.GET.get('Tell', '')

            try:
                member = Member.objects.get(username=username, email=email, Tell=Tell)
                return JsonResponse({'password': member.password})

            except ObjectDoesNotExist:
                return JsonResponse({'error': '비밀번호를 찾을 수 없습니다.'})

        return render(request, 'member/find.html')

# 회원가입 시 아이디 중복확인(DB비교)
def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')

        try:
            existing_member = Member.objects.get(username=username)
            return JsonResponse({'message': '이미 존재하는 아이디입니다.', 'status': 'error'})

        except Member.DoesNotExist:
            return JsonResponse({'message': '사용 가능한 아이디입니다.', 'status': 'success'})

    return JsonResponse({'message': '잘못된 요청입니다.', 'status': 'error'})

#mypage
@login_required
def mypage(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            update_form = UpdateProfileForm(request.POST)
            if update_form.is_valid():
                email = update_form.cleaned_data['email']
                Tell = update_form.cleaned_data['Tell']
                new_password = update_form.cleaned_data['new_password']
                confirm_password = update_form.cleaned_data['confirm_password']

                if new_password == confirm_password:
                    # 회원정보 수정
                    request.user.email = email
                    request.user.Tell = Tell
                    if new_password:
                        request.user.set_password(new_password)     # 새로운 비밀번호 업데이트
                    request.user.save()
                    success_message = '회원 정보가 성공적으로 수정되었습니다.'
                else:
                    error_message = '새 비밀번호와 비밀번호 확인이 일치하지 않습니다.'
            else:
                error_message = '양식이 유효하지 않습니다.'
        elif action == 'withdraw':
            # 회원 탈퇴
            request.user.delete()           # 등록된 사용자 삭제
            success_message = '회원 탈퇴가 완료되었습니다.'
            return redirect(reverse('member:login'))
    else:   # initial : 폼 생성 초기데이터 지정(이메일,연락처는 기본적으로 input 박스에 제공)
        update_form = UpdateProfileForm(initial={'email': request.user.email, 'Tell': request.user.Tell})

    return render(request, 'member/mypage.html', {'update_form': update_form, 'success_message': success_message, 'error_message': error_message})