from django import forms
from .models import Post, Tag


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

    def save(self, commit=True):
        post = super().save(commit=False)
        post.author = self.user
        if commit:
            post.save()
            self.save_m2m()
        return post


class EditPostForm(NewPostForm):
    pass

