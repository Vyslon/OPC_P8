from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur",
            max_length=150,
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            required=True
            )
    password = forms.CharField(label="Mot de passe",
            max_length=50,
            widget=forms.PasswordInput(attrs={'class': 'form-control'}),
            required=True
            )
    email = forms.EmailField(label="e-mail",
        max_length=150,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
        )

class AuthenticationForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur",
            max_length=150,
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            required=True
            )
    password = forms.CharField(label="Mot de passe",
            max_length=50,
            widget=forms.PasswordInput(attrs={'class': 'form-control'}),
            required=True
            )
