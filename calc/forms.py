# calc/forms.py
from django import forms

from .models import ExcelFile

class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file']

class ExcelFileUploadForm(forms.Form):
    excel_file = forms.FileField()

#Add other forms as needed
