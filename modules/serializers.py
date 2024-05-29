from modules.models import Module, Page
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from account.models import UserProgress


class ModuleSerializer(serializers.ModelSerializer):
    total_pages = serializers.SerializerMethodField()
    total_completed_pages = serializers.SerializerMethodField()

    class Meta:
        model = Module
        exclude = ["created_at", "updated_at"]

    def get_total_pages(self, obj):
        return obj.pages.count()

    def get_total_completed_pages(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Page)
            progress = UserProgress.objects.filter(
                content_type=content_type,
                object_id__in=obj.pages.all().values_list("id", flat=True),
                user=request.user,
                is_completed=True,
            ).count()
            return progress
        return 0


class PageSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = "__all__"

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Page)
            progress = UserProgress.objects.filter(
                content_type=content_type,
                object_id=obj.id,
                user=request.user,
                is_completed=True,
            ).exists()
            return progress
        return False


class ModuleUserProgressSerializer(serializers.ModelSerializer):
    module_details = serializers.SerializerMethodField()

    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.filter(model="game"),
        slug_field="model",
        write_only=True,
    )
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserProgress
        fields = ["id", "content_type", "object_id", "is_completed", "module_details"]

    def get_module_details(self, obj):
        """Serialize the game details if the related object is a Game"""
        if isinstance(obj.content_object, Module):
            return ModuleSerializer(obj.content_object, context=self.context).data
        return None
