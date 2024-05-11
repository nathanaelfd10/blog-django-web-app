from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    TITLE_MAX_LENGTH = 200

    class Meta:
        model = Post
        fields = ('title', 'text',)
    
    def clean(self):
        super(PostForm, self).clean()

        title = self.cleaned_data.get('title')
        # text = self.cleaned_data.get('text')

        if len(title) > self.TITLE_MAX_LENGTH:
            self._errors['username'] = self.error_class([
                "Maximum title length is {title_max_length} {character_or_characters}".format(title_max_length = self.TITLE_MAX_LENGTH, character_or_characters="character" if len(title) <= 1 else "characters")
            ])

        return self.cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        