# calc/forms.py
from django import forms

from .models import ExcelFile


class ExcelFileForm(forms.ModelForm):
    # excel_file = forms.FileField()
    class Meta:
        model = ExcelFile
        fields = ['file']


    def save(self, commit=True, uploaded_by=None):
        instance = super().save(commit=False)
        instance.uploaded_by = uploaded_by
        if commit:
            instance.save()
        return instance
# class ExcelFileUploadForm(forms.ModelForm):
#     excel_file = forms.FileField()
#
#     class Meta:
#         model = ExcelFile
#         fields = ['file']

# Add other forms as needed
