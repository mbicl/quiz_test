from django.forms import ModelForm
from .models import Test


class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = "__all__"
