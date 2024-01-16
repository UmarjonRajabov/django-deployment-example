# calc/forms.py
from django import forms


class ExcelFileUploadForm(forms.Form):
    excel_file = forms.FileField()

# Add other forms as needed
