from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='',widget = forms.TextInput(attrs={'placeholder':'Email Address', 'class':'form-control'}))
    first_name = forms.CharField(max_length= 100, label='',widget = forms.TextInput(attrs={'placeholder':'First Name', 'class':'form-control'}))
    last_name = forms.CharField(max_length= 100, label='',widget = forms.TextInput(attrs={'placeholder':'Last Name', 'class':'form-control'}))


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','first_name', 'last_name', 'email', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs['class'] = 'form-control'
        self.fields["username"].widget.attrs['placeholder'] = 'Username'
        self.fields["username"].label = ''

        self.fields["password1"].widget.attrs['class'] = 'form-control'
        self.fields["password1"].widget.attrs['placeholder'] = 'Enter Your Password'
        self.fields["password1"].label = ''

        self.fields["password2"].widget.attrs['class'] = 'form-control'
        self.fields["password2"].widget.attrs['placeholder'] = 'Enter Your Password Again'
        self.fields["password2"].label = ''

