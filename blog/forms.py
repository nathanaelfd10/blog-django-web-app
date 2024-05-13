from django import forms

from .models import Post, Comment
from django.forms import ValidationError

class PostForm(forms.ModelForm):
    TITLE_MAX_LENGTH = 5

    class Meta:
        model = Post
        fields = ('title', 'text',)

    def has_numbers(self, inputString):
        return any(char.isdigit() for char in inputString)
    
    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     title = title.lower()
    #     return title
    
    def clean(self):
        super(PostForm, self).clean()

        title = self.cleaned_data.get('title')
        # text = self.cleaned_data.get('text')

        if len(title) > self.TITLE_MAX_LENGTH:
            message = "Title length can't exceed {title_max_length} {character_or_characters}".format(title_max_length = self.TITLE_MAX_LENGTH, character_or_characters="character" if len(title) <= 1 else "characters")
            raise ValidationError(message, code="invalid")
            # self._errors['title'] = self.error_class([
            #     "Maximum title length is {title_max_length} {character_or_characters}".format(title_max_length = self.TITLE_MAX_LENGTH, character_or_characters="character" if len(title) <= 1 else "characters")
            # ])
        
        # if self.has_numbers(title):
        #     raise ValidationError("Title can't have number", code="invalid")

            # self._errors['title'] = self.error_class([
            #         "Title can't contain number"
            # ])
        
        return self.cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        