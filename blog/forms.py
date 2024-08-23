from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for comments

    Args:
        forms (_type_): base class
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
