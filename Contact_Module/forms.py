from django import forms
from .models import ContactUs, UserProfile


class ContactUsForm(forms.Form):
    full_name = forms.CharField(
        label='نام و نام خانوادگی',
        max_length=50,
        error_messages={
            'required': 'لطفا نام و نام خانوادگی خود را وارد کنید',
            'max_length': 'نام و نام خانوادگی نمی تواند بیشتر از 50 کاراکتر باشد'
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی'
        })
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        }),
        required=False
    )
    title = forms.CharField(
        label='عنوان',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان'
        }),
        required=False
    )
    message = forms.CharField(
        label='متن پیام',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'متن پیام',
            'id': 'message',
            'rows': '5'
        }),
        required=False
    )


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs

        fields = ['full_name', 'title', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'id': 'message'
            })
        }

        error_messages = {
            'full_name': {
                'required': 'نام و نام خانوادگی باید پر شده باشد'
            }
        }


# class ProfileModelForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
#         widgets = {
#             'image': forms.FileInput(attrs={
#                 'class': 'form-control'
#             })
#         }
#         labels = {
#             'image': 'عکس پروفایل'
#         }
