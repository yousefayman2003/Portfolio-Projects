from typing import Any
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User, PostModel, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='', required=True,  widget=forms.TextInput(
        attrs={'placeholder': 'Email Address', 'rows': 1}), help_text='Required. add a valid email address.')
    phone = forms.CharField(label='', max_length=11, required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'rows': 1}), help_text='Required. add a phone number.')
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required. add a first name.', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'rows': 1}))
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required. add a last name', widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'rows': 1}))
    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2023, 1960, -1)))
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect())

    password1 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Password', 'rows': 1}))
    password2 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Confirm Password', 'rows': 1}))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        print(len(phone),  phone)
        if len(phone) == 11:
            return phone
        raise forms.ValidationError(
            'Phone number must be exactly 11 digits')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        print(len(phone),  phone)
        if len(phone) == 11:
            return phone
        raise forms.ValidationError(
            'Phone number must be exactly 11 digits')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone',
                  'password1', 'password2', 'date_of_birth', 'gender']

    # For removing help text

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegisterForm, self).__init__(*args, **kwargs)

        for name in ['first_name', 'last_name', 'email', 'phone',
                     'password1', 'password2', 'date_of_birth', 'gender']:
            self.fields[name].help_text = None


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if authenticate(email=email, password=password):
                pass

            else:
                raise forms.ValidationError('Invalid Login')


class PostingModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = PostModel
        fields = ['title', 'content']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        image = forms.ImageField()
        about = forms.CharField()
        fields = ['email', 'phone', 'image', 'about']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['email', 'phone', 'image']:
            self.fields[fieldname].help_text = None


class PostingUpdateForm(forms.ModelForm):

    class Meta:
        model = PostModel
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Add comment here.....'}))

    class Meta:
        model = Comment
        fields = ['content',]


class like_clicked(forms.ModelForm):
    button = forms.CharField(widget=forms.HiddenInput(), initial='Submit')

    class Meta:
        model = PostModel
        fields = ['button',]
