from django.forms import ModelForm
from .models import Test, TestGroup


class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = "__all__"

    def __init__(self,user=None,**kwargs):
        super(TestCreateForm, self).__init__(**kwargs)
        if user:
            self.fields['test_group'].queryset = TestGroup.objects.filter(owner__username=user.username).all()