from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'required': '',
                'class': 'input',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError("Field cannot be empty")


class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Full Name',
                'required': '',
                'class': 'input',
            }
        )
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'required': '',
                'class': 'input',
            }
        )
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Phone Number',
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
    password = forms.CharField(
        help_text="Password must not be less tha 8 characters",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'required': '',
                'class': 'input',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Verify Password',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        full_name = cleaned_data.get('full_name')
        username = cleaned_data.get('username')
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not full_name or not username or not phone_number or not email or not password or not confirm_password:
            raise forms.ValidationError("Field cannot be empty")
        elif len(full_name) < 2 or len(full_name) > 250:
            raise forms.ValidationError("Full Name must be between 2-250")
        elif len(password) < 8 or len(confirm_password) < 8:
            raise forms.ValidationError("Password cannot be less than 8 characters")
        elif password != confirm_password:
            raise forms.ValidationError("Password does not match")


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
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

    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if not username or not email:
            raise forms.ValidationError("Field cannot be empty")


class PasswordRetrievalForm(forms.Form):
    password = forms.CharField(
        max_length=12,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Recovery Password',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(PasswordRetrievalForm, self).clean()
        password = cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Field cannot be empty")


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'required': '',
                'class': 'input',
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Verify Password',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not password or not confirm_password:
            raise forms.ValidationError("Field cannot be empty")


class AmountForm(forms.Form):
    amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Amount',
                'required': '',
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(AmountForm, self).clean()
        amount = cleaned_data.get('amount')
        if not amount:
            raise forms.ValidationError("Field cannot be empty")


class TextForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter Message...',
                'required': '',
                'class': 'input',
                'cols': 50,
                'style': 'height:200px',
            }
        )
    )

    def clean(self):
        cleaned_data = super(TextForm, self).clean()
        message = cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Field cannot be empty")

