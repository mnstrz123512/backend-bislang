from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from account.models import UserProgress
from modules.models import Page


class PageUserProgressAdmin(admin.ModelAdmin):
    list_display = ["get_page", "user", "is_completed"]
    search_fields = ["user__username"]
    list_filter = ["is_completed"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        page_content_type = ContentType.objects.get_for_model(Page)
        return qs.filter(content_type=page_content_type)

    def get_page(self, obj):
        if isinstance(obj.content_object, Page):
            return obj.content_object
        return "Not a Page"

    get_page.short_description = "Page"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(model="page")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
