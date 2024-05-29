from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.response import Response

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Exists, OuterRef

from account.models import UserAchievement
from modules.serializers import PageSerializer
from modules.models import Page
from account.models import UserProgress

from .serializers import ModuleSerializer
from .models import Module
from .serializers import ModuleUserProgressSerializer


class ModuleViewset(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    @action(detail=True, methods=["get"])
    def pages(self, request, pk=None):
        module = self.get_object()
        pages = module.pages.all()
        pages_serializer = PageSerializer(
            pages, many=True, context={"request": request}
        )
        return Response(pages_serializer.data)

    @action(detail=True, methods=["get"], url_path="pages/(?P<page_pk>\d+)")
    def page_detail(self, request, pk=None, page_pk=None):
        module = self.get_object()
        page = get_object_or_404(module.pages, pk=page_pk)
        serializer = PageSerializer(page, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="pages/(?P<page_id>\d+)/progress")
    def update_progress(self, request, pk=None, page_id=None):
        module = self.get_object()
        page = get_object_or_404(Page, pk=page_id, module=module)
        user = request.user

        page_content_type = ContentType.objects.get_for_model(Page)

        with transaction.atomic():
            progress, created = UserProgress.objects.get_or_create(
                user=user, content_type=page_content_type, object_id=page.id
            )

            serializer = ModuleUserProgressSerializer(
                progress, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if module.achievement:
                all_completed = (
                    module.pages.all()
                    .annotate(
                        completed=Exists(
                            UserProgress.objects.filter(
                                user=user,
                                content_type=page_content_type,
                                object_id=OuterRef("pk"),
                                is_completed=True,
                            )
                        )
                    )
                    .filter(completed=False)
                    .exists()
                    == False
                )

                if all_completed:
                    if not UserAchievement.objects.filter(
                        user=user, achievement__module=module
                    ).exists():
                        achievement = module.achievement
                        UserAchievement.objects.create(
                            user=user, achievement=achievement
                        )

            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
