from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        # Adding html <input/> attributes. Found here:
        # https://stackoverflow.com/questions/62242570/adding-placeholder-to-usercreationform-in-django
        widgets = {
            'username': TextInput(attrs={
                        'class':'form-control',
                        'placeholder':'E.g. kirill_zelensky',
                }),
            'email': TextInput(attrs={
                        'class':'form-control',
                        'placeholder':'Your email here',
                })
        }