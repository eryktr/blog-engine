from django import forms
from .models import Post, Tag
import datetime


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['tags'].queryset = Tag.objects.all()

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

    @staticmethod
    def trim_content(content):
        length = 500
        return content[:length] + "..." if len(content) > length else content

    def save(self, commit=True):
        post = super().save(commit=False)
        post.post_date = datetime.datetime.now()
        post.last_update = datetime.datetime.now()
        post.trimmed_content = self.trim_content(post.content)
        post.author = self.user
        if commit:
            post.save()
        return post


class EditPostForm(NewPostForm):
    def save(self, commit=True):
        post = super(forms.ModelForm, self).save(commit=False)
        post.last_update = datetime.datetime.now()
        post.trimmed_content = self.trim_content(post.content)
        if commit:
            post.save()
        return post

