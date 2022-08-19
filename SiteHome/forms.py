from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Name',
                'required': '',
                'class': 'input',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'required': '',
                'class': 'input',
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Message',
                'required': '',
                'class': 'input',
                'cols': 50,
                'style': 'height:100px',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name or not email or not message:
            raise forms.ValidationError("Field cannot be empty")