# from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields=["email","password"]
