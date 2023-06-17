from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField


class TestGroup(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='test_group')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Test(models.Model):
    question = RichTextUploadingField()
    option1 = RichTextUploadingField()
    option2 = RichTextUploadingField()
    option3 = RichTextUploadingField()
    option4 = RichTextUploadingField()
    ans = models.IntegerField(default=1, validators=(MinValueValidator(1), MaxValueValidator(4)))
    test_group = models.ForeignKey(TestGroup, on_delete=models.CASCADE, related_name='test')

    def __str__(self):
        return self.question
