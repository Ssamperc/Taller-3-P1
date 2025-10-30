from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(label="Buscar película", max_length=250)
