# board/forms.py
from django import forms
<<<<<<< HEAD
from member.models import Board
=======
from board.models import Board
>>>>>>> 5300eb95c0d7ea7cc17b9ef5baf1824939fa8c83

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'category', 'contents', 'file_upload']