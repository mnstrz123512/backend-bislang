from django import forms
from account.models import Achievement
from games.models import Type


class TypeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    achievement = forms.ModelChoiceField(
        queryset=Achievement.objects.all(), required=False
    )

    class Meta:
        model = Type
        fields = "__all__"
