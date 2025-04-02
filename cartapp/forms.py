from django import forms
from .models import ShippingAddress
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["name","email", "city", "postal_code", "country","address","phone","is_current_address"]
        widgets = {
            
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols":5}),
            'is_current_address': forms.RadioSelect()
           
        }
class AddressupdateForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ["name","email", "city", "postal_code", "country","address","phone"]
        widgets = {
            
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 5, "cols":5}),
           
        }
            
    