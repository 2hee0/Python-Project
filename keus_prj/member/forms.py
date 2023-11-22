from django import forms

class MemberForm(forms.Form):
    member_id = forms.CharField(max_length=200)
    member_pw = forms.CharField(max_length=200)
    tell = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    PasswordOK = forms.CharField(max_length=200)