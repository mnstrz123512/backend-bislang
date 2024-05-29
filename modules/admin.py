from django import forms
from django.contrib import admin

from account.models import Achievement
from modules.admins.progress.admin import PageUserProgressAdmin
from .models import Module, Page, PageUserProgress

# Register your models here.


class PageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)
    audio = forms.FileField(required=False)

    class Meta:
        model = Page
        fields = "__all__"


class ModuleForm(forms.ModelForm):
    achievement = forms.ModelChoiceField(
        queryset=Achievement.objects.all(),
        required=False,
        empty_label="Select an achievement",
    )

    class Meta:
        model = Module
        fields = "__all__"


class PageInline(admin.StackedInline):
    model = Page
    form = PageForm
    extra = 0


class ModuleAdmin(admin.ModelAdmin):
    inlines = [PageInline]
    form = ModuleForm


admin.site.register(Module, ModuleAdmin)
admin.site.register(PageUserProgress, PageUserProgressAdmin)
