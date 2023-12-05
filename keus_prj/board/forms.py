# board/forms.py
from django import forms
# 231130 하승우 board.models -> .models 수정
from .models import Board, Comment

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'category', 'contents', 'file_upload']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']