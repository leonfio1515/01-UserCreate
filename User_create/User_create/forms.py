from django import forms
from DB.models import *

##################################################################


class UserCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control text-center'

    class Meta:
        model = Users
        fields = (
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Username",
                    "autofocus": "True",
                    "type": "text",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Nombre",
                    "type": "text",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Apellido",
                    "type": "text",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "mail@example.com",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Password",
                }
            ),
        }

        exclude = [
            "address",
            "number_address",
            "city",
            "country",
            "phone_number",
            "dni",
            "image_user",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        return instance
