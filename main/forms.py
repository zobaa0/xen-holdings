from django import forms
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, required=True,
                           widget=forms.TextInput(attrs={                             
                               'id': 'name',
                               'placeholder': 'Your Name *'
                           }))
    email = forms.EmailField(max_length=30, required=True,
                             widget=forms.TextInput(attrs={                             
                                 'id': 'email',
                                 'placeholder': 'Your Email *'
                             }))
    subject = forms.CharField(required=True, max_length=20,
                              widget=forms.TextInput(attrs={                                 
                                  'id': 'subject',
                                  'placeholder': 'Subject *'
                              }))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={       
        'id': 'message',
        'rows': 8,
        'cols': 30,
        'placeholder': 'Enter Your Message *'
    }))

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()
        name = cl_data.get('name').strip()
        email = cl_data.get('email')
        subject = cl_data.get('subject')
        # Compose mail
        message = f'{name.capitalize()} with email {email} just sent you a mail.\n'
        message += f"\nSubject: '{subject}'\n\n"
        message += cl_data.get('message')
        message += f'\n\n\nsiteName ContactUs Page'
        message += f"\nsiteName.com"
        # Return composed mail data
        return subject, message

    def send(self):
        subject, message = self.get_info()
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['okonkwogodspower@yahoo.com'],
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
