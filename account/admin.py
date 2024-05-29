from django import forms
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Achievement, CustomUser, Badge, UserAchievement


class UserAchievement(admin.TabularInline):
    model = UserAchievement
    extra = 0


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("profile_image",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("profile_image",)}),)
    inlines = [UserAchievement]


class AchievementAdmin(admin.ModelAdmin):
    model = Achievement
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["-created_at"]


class BadgeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)


class BadgeAdmin(admin.ModelAdmin):
    model = Badge
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["-created_at"]
    form = BadgeForm


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Badge, BadgeAdmin)
