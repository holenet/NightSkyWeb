from django import forms

from judge.models import Submission


class ProblemForm(forms.Form):
    title = forms.CharField()
    testcases = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class TestcaseAddForm(forms.Form):
    testcases = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('code_file', )
