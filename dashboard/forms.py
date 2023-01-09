from django import forms
from django.contrib.auth import get_user_model
from .models import Subscription, Plan, Wallet, Withdrawal, Transfer

# Custom user model
UserModel = get_user_model()


class BasicInfo(forms.ModelForm):
    """Update User's basic info"""
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control form-control-md',
                                     'id': 'fn',
                                     'placeholder': 'John'
                                 }))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control form-control-md',
                                    'id': 'fn',
                                    'placeholder': 'Doe'
                                }))
    email = forms.EmailField(max_length=30, required=True,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control form-control-md',
                                 'id': 'fn',
                                 'placeholder': 'Doe'
                             }))

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email']


class AddressInfo(forms.ModelForm):
    """Update User's address info"""
    country = forms.CharField(required=True, max_length=2,
                              error_messages={
                                  'required': 'Country field cannot be empty'
                              },
                              widget=forms.Select(choices=UserModel.COUNTRIES, attrs={
                                  'class': 'form-select form-select-md',
                                  'id': 'country',
                                  'style': 'color: #000;'
                              }))
    phone = forms.CharField(max_length=20, required=True,
                            error_messages={
                                'required': 'Phone number field cannot be empty'
                            },
                            widget=forms.TextInput(attrs={
                                'class': 'form-control form-control-md',
                                'id': 'phone_no',
                                'placeholder': '+1 (256)...'
                            }))
    address = forms.CharField(max_length=60, required=True,
                              error_messages={
                                  'required': 'Address field cannot be empty'
                              },
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control form-control-md',
                                  'id': 'address',
                                  'placeholder': 'Enter your address'
                              }))

    class Meta:
        model = UserModel
        fields = ['country', 'phone', 'address']


class DeleteAccount(forms.ModelForm):
    """Delete User's account"""
    del_account = forms.BooleanField(required=False)
    del_account.widget.attrs.update({'class': 'form-check-input',
                                     'id': 'delete_account'})

    class Meta:
        model = UserModel
        fields = ['del_account']


class DepositForm(forms.ModelForm):
    plan = forms.ModelChoiceField(queryset=Plan.objects.all(),
                                  empty_label="Select Plan",
                                  to_field_name='plan_name',
                                  required=True,
                                  widget=forms.Select(attrs={
                                      'class': 'form-select form-select-md',
                                      'id': 'plans',
                                  }))
    sub_method = forms.CharField(required=True,
                                 widget=forms.Select(choices=Subscription.SUB_METHOD,
                                                     attrs={
                                                         'class': 'form-select form-select-md',
                                                         'id': 'method',
                                                     }))
    sub_currency = forms.CharField(required=True,
                                   widget=forms.Select(choices=Subscription.SUB_CURRENCY,
                                                       attrs={
                                                           'class': 'form-select form-select-md',
                                                           'id': 'currency',
                                                       }))
    sub_amount = forms.DecimalField(required=True,
                                    widget=forms.NumberInput(attrs={
                                        'class': 'form-control form-control-md',
                                        'id': 'amount',
                                        'placeholder': "Min - $80.00",
                                    }))

    class Meta:
        model = Subscription
        fields = ['plan', 'sub_method', 'sub_currency', 'sub_amount']


class WalletForm(forms.ModelForm):
    type = forms.CharField(required=True,
                           widget=forms.Select(choices=Wallet.NETWORK,
                                               attrs={
                                                   'class': 'form-select form-select-md',
                                                   'id': 'w-network',
                                               }))
    address = forms.CharField(required=True, max_length=60,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control form-control-md',
                                  'id': 'w-address',
                                  'placeholder': 'Wallet Address'
                              }))

    class Meta:
        model = Wallet
        exclude = ['user']

    def full_clean(self):
        """Validate unique constraints (user, type)"""
        super(WalletForm, self).full_clean()
        try:
            self.instance.validate_unique()
        except:
            self.add_error(
                'address', 'Wallet address with this name already exists.')


class WithdrawalForm(forms.ModelForm):
    wallet = forms.ModelChoiceField(queryset=Wallet.objects.all(),
                                    empty_label="Choose Wallet",
                                    to_field_name='type',
                                    required=True,
                                    widget=forms.Select(attrs={
                                        'class': 'form-select form-select-md',
                                        'id': 'w-wallet',
                                    }))
    amount = forms.DecimalField(required=True,
                                widget=forms.NumberInput(attrs={
                                    'class': 'form-control form-control-md',
                                    'id': 'w-amount',
                                    'placeholder': "Min - $80.00",
                                }))

    class Meta:
        model = Withdrawal
        fields = ['wallet', 'amount']

    def __init__(self, *args, **kwargs):
        """Filter wallets based on user instance"""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)


class TransferForm(forms.ModelForm):
    """Form definition for Transfer."""

    class Meta:
        """Meta definition for TransferForm."""

        model = Transfer
        fields = ('username', 'amount')

    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control form-control-md',
                                   'id': 'r_username',
                                   'placeholder': "Receiver's Username",
                               }))
    amount = forms.DecimalField(required=True,
                                widget=forms.NumberInput(attrs={
                                    'class': 'form-control form-control-md',
                                    'id': 't_amount',
                                    'placeholder': "$0.00",
                                }))
