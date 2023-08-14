from django.forms import TextInput, CharField

from .models import Post, Category, User, Note, Comment
from .models import Debate
from django import forms
from MainApp.models import Profile, Message
# hard-coded version of selection list of categories (not used)
#choices = [('economics', 'economics'), ('philosophy', 'philosophy'), ('medicine', 'medicine'), ('politics', 'politics')]
choices = Category.objects.all().values_list('category', 'category')
choice_list = []
for item in choices:
    choice_list.append(item)

authors = Post.objects.all().values_list('author', 'author')
author_list = []
for person in authors:
    author_list.append(person)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Debate
        fields = ['category', 'title', 'description']

class PostForm(forms.ModelForm):
    '''def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = user.profile.field'''
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'header_image', 'status')
        #exclude = ('author', 'slug', 'publish', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'username', 'id':'user', 'type':'hidden'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class NoteForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=forms.widgets.Textarea(attrs={
                               "placeholder":"Enter Note",
                               "class":"form-control"
                           }),
                           label="",)

    class Meta:
        model = Note
        exclude = ("profile","user")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commenter_name','body')

        widgets = {
            'commenter_name':forms.Select(choices=author_list, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DebateForm(forms.ModelForm):
    class Meta:
        model = Debate
        fields = ('category', 'author', 'opponent', 'description', 'title')

        widgets = {
            'category':forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'author':forms.Select(choices=author_list, attrs={'class': 'form-control'}),
            'opponent':forms.Select(choices=author_list, attrs={'class': 'form-control'}),
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']