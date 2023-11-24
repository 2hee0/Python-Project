from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Member
from .forms import MemberForm

def join(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member_data = form.cleaned_data
            # 비밀번호 확인 부분
            if member_data['password'] == member_data['PasswordOK']:
                Member.objects.create(
                    username=member_data['username'],
                    password=member_data['password'],
                    Tell=member_data['Tell'],
                    email=member_data['email']
                )
                return redirect(reverse('login'))  # 가입 성공 페이지(reverse 함수사용 -> member/login 으로 이동)
            else:
                # 비밀번호가 일치하지 않을 경우 에러 메시지 추가
                form.add_error('PasswordOK', '비밀번호가 일치하지 않습니다.')
    else:
        form = MemberForm()

    return render(request, 'member/join.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        members = Member.objects.filter(username=username, password=password)
        if members.exists():
            # 로그인 처리
            member = members.first()  # 검색된 회원중 첫번째 회원을 가져옴
            request.session['username'] = member.username
            return redirect(reverse('header'))
        else:
            # 로그인 실패
            return render(request, 'member/login.html', {'error_message': '아이디 또는 비밀번호를 잘못 입력했습니다.'})

    return render(request, 'member/login.html')

# 로그인 성공시 메인페이지로 이동(지금은 임시로 member/header.html 로 )
def header(request):
    return render(request, 'member/header.html')

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

def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')

        try:
            existing_member = Member.objects.get(username=username)
            return JsonResponse({'message': '이미 존재하는 아이디입니다.', 'status': 'error'})

        except Member.DoesNotExist:
            return JsonResponse({'message': '사용 가능한 아이디입니다.', 'status': 'success'})

    return JsonResponse({'message': '잘못된 요청입니다.', 'status': 'error'})