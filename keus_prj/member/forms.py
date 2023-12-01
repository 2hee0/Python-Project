from django import forms

class MemberForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)  # 수정된 부분
    password = forms.CharField(max_length=128,required=True)
    PasswordOK = forms.CharField(max_length=128,required=True)
    Tell = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=254,required=True)

# mypage 회원정보 수정(업데이트)을 위한 UpdateForm 설정
class UpdateProfileForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    Tell = forms.CharField(max_length=20, required=True)
    new_password = forms.CharField(max_length=128, required=True)
    confirm_password = forms.CharField(max_length=128, required=True)

