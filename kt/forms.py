from django import forms
from .models import Kontakt

class KontaktForm(forms.ModelForm):

    class Meta:
        model = Kontakt
        fields = '__all__'