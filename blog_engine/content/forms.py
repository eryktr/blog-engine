from django import forms
from .models import Post
import datetime


class NewPostForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(forms.ModelForm, self).__init__(*args, **kwargs)


    content = forms.CharField(
        label="Content:",
        widget=forms.Textarea(
            attrs={
                'id': 'post-content',
                'rows': 20,
                'cols': 150
            }
        )

    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True):
        post = super().save(commit=False)
        post.post_date = datetime.datetime.now()
        post.last_update = datetime.datetime.now()
        post.author = self.user
        if commit:
            post.save()
        return post
