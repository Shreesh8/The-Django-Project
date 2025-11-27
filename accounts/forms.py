from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username = username, password = password)
            if not user:
                raise forms.ValidationError('Wrong password or username')
        return super(LoginForm, self).clean()

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)
    password_repeat = forms.CharField(max_length=100, label='Password repeat', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_repeat',
        ]


    def clean_password_repeat(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password and password_repeat and password != password_repeat:
            self.add_error("password_repeat", "passwords do not match.")
        return password_repeat

class AdminUsersPasswords(forms.ModelForm):
    old_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Current password"
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="New password"
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Repeat new password"
    )

    class Meta:
        model = User
        fields = ["old_password","password","confirm_password"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("instance")   # the User instance
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()

        old = cleaned.get("old_password")
        new = cleaned.get("password")
        confirm = cleaned.get("confirm_password")

        if new or confirm:
            if not old:
                self.add_error("old_password", "Enter your current password.")
            elif not check_password(old, self.user.password):
                self.add_error("old_password", "Wrong current password.")
            if new != confirm:
                self.add_error("confirm_password", "New paswords do not match.")

        return cleaned