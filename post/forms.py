from django import forms
from post.models import Post, Comment, ContactInfo

#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Field, Submit
#from django_recaptcha.fields import ReCaptchaField

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "desc",
            "image",
            "video",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]

class ContactusForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = [
            'name',
            'surname',
            'adress',
            'user_gender',
            'email',
        ]

#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_method = 'post'
#
#        self.helper.layout = Layout(
#            Field('name', css_class='form-control', template='bootstrap4/layout/field.html'),
#            Field('content', css_class='form-control', template='bootstrap4/layout/field.html'),
#            Submit('submit', 'Comment', css_class='btn btn-primary')
#        )