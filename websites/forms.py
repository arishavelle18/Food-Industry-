from django.forms import ModelForm
from  .models import Profiles

class UserForm(ModelForm):
    class Meta:
        model = Profiles
        fields=["name","email"]
