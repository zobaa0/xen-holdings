from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, 
                                       PasswordChangeForm, PasswordResetForm)
from django.utils.translation import gettext_lazy as _

# Custom user model
UserModel = get_user_model()

class NewUserForm(UserCreationForm):
    """
    New User Registration Form
    """
    username = forms.CharField(max_length=15,
                               required=True,
                               widget=forms.TextInput(attrs={
                                    'placeholder': 'johnny',
                                    'class': 'form-control form-control-md',
                                    'id': 'username',
                                }))
    email = forms.EmailField(required=True,
                             max_length=30,
                             help_text="Enter a valid email address",
                             widget=forms.TextInput(attrs={
                                'placeholder': 'johnny@email.com',
                                'class': 'form-control form-control-md',
                                'id': 'email_add'
                            }))
    password1 = forms.CharField(max_length=24,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Enter Password',
                                    'class': 'form-control form-control-md',
                                    'id': 'password1',
                                }))
    password2 = forms.CharField(max_length=24,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Confirm Password',
                                    'class': 'form-control form-control-md',
                                    'id': 'password2',
                                }))
    # terms = forms.BooleanField(required=True,
    #                             error_messages={
    #                             'required': 'You need to agree to the company terms.',
    #                           })
    # terms.widget.attrs.update({'class': 'form-check-input',
    #                            'id': 'terms'})

    class Meta:
        model = UserModel
        fields = ("username", 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
        """Case in-sensitive username"""
        cleaned_data = super(NewUserForm, self).clean()
        username = cleaned_data.get('username')
        if username and UserModel.objects.filter(username__iexact=username).exists():
            self.add_error("username", "A user with this username already exists.")
        return cleaned_data



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(error_messages={
                                'required': 'Invalid Username or Password.',
                              },
                              widget=forms.TextInput(
                              attrs={'class': 'form-control form-control-md',
                                'id': 'username',
                                'placeholder': 'Username or Email'}
                              ))

    password = forms.CharField(error_messages={
                                'required': 'Invalid Username or Password.',
                              },
                              widget=forms.PasswordInput(
                              attrs={'class': 'form-control form-control-md',
                                'id': 'password',
                                'placeholder': 'Password'}
                              ))
    error_messages = {
        'invalid_login': _("Please enter a valid %(username)s and password."),
        'inactive': _("Your account has been deactivated."),
    }


class PasswordChange(PasswordChangeForm):
    """Change User's Password"""
    old_password = forms.CharField(max_length=24,
                                   required=True,
                                   widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Enter old password',
                                    'autofocus': True,
                                    'class': 'form-control form-control-md',
                                    'id': 'old_password',
                                   }))
    new_password1 = forms.CharField(max_length=24,
                                    required=True,
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'New password',
                                        'class': 'form-control form-control-md',
                                        'id': 'new_password1',
                                    }))
    new_password2 = forms.CharField(max_length=24,
                                    required=True,
                                    widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Confirm new password',
                                        'class': 'form-control form-control-md',
                                        'id': 'new_password2',
                                    }))


class ResetPasswordForm(PasswordResetForm):
    """"Reset User's Password"""
    email = forms.EmailField(required=True,
                             max_length=30,
                             help_text="Enter a valid email address",
                             widget=forms.TextInput(attrs={
                                'placeholder': 'Enter Email',
                                'class': 'form-control form-control-md',
                                'id': 'email'
                            }))