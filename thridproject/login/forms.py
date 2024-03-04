from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','content']

#여기 폼의 fields는 html에서 해당 폼을 쓸 때, fields에 명시해놓은 변수만 방문자가 써서 서버로 보낼 수 있다라는 뜻인 듯.
#views.py에서는 여기에서 명시한 변수 외의 model에 포함된 다른 변수를 다룰 수 있음. 
#다시 말하자면, 여기 form은 html 방문자가 쓸 부분만 명시해놓은 것
        
class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=['content']
        


