# board/forms.py
from django import forms
from board.models import Board

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'category', 'contents', 'file_upload']