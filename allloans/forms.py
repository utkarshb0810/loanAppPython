from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['bank_name', 'start_date', 'end_date', 'bank_account_number', 'file_path']
        
        widgets ={
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
             'file_path': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }