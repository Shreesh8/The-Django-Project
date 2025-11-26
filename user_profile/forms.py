from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class UserProfileForm(forms.ModelForm):
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
        fields = ["username"]

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