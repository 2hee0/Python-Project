from django.core.exceptions import ObjectDoesNotExist
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
            return redirect('/')
        else:
            # 로그인 실패
            return render(request, 'member/login.html', {'error_message': '아이디 또는 비밀번호를 잘못 입력했습니다.'})

    return render(request, 'member/login.html')