from django.forms import ModelForm
from .models import Voter


class VoterForm(ModelForm):
    class Meta:
        model = Voter
        # fields = "__all__"
        exclude = ("id", "assembly")


