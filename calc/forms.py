# calc/forms.py
from django import forms

from .models import ExcelFile

class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file']

# class ExcelFileUploadForm(forms.ModelForm):
#     excel_file = forms.FileField()
#
#     class Meta:
#         model = ExcelFile
#         fields = ['file']

#Add other forms as needed
