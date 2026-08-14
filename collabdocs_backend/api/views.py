from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction, IntegrityError
from django.db.models import Count, Q
from .models import User, Workspace, WorkspaceMember, Document, DocumentVersion, Comment, Tag, AuditLog
from .serializers import (UserSerializer, WorkspaceSerializer, WorkspaceMemberSerializer, 
                          DocumentSerializer, DocumentVersionSerializer, CommentSerializer, 
                          TagSerializer, AuditLogSerializer)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            workspace = serializer.save(owner=self.request.user)
            WorkspaceMember.objects.create(
                workspace=workspace,
                user=self.request.user,
                role=WorkspaceMember.RoleChoices.ADMIN
            )

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        workspace = self.get_object()
        stats = Document.objects.filter(workspace=workspace).aggregate(
            total_docs=Count('id'),
            published_docs=Count('id', filter=Q(status=Document.StatusChoices.PUBLISHED))
        )
        return Response(stats)

class WorkspaceMemberViewSet(viewsets.ModelViewSet):
    queryset = WorkspaceMember.objects.select_related('workspace', 'user').all()
    serializer_class = WorkspaceMemberSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"error": "This user is already a member of this workspace."}, 
                status=status.HTTP_409_CONFLICT
            )

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        queryset = Document.objects.select_related('workspace', 'created_by').all()
        search = self.request.query_params.get('search', None)
        status_filter = self.request.query_params.get('status', None)
        
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset

    def perform_create(self, serializer):
        with transaction.atomic():
            doc = serializer.save(created_by=self.request.user)
            version_number = doc.versions.count() + 1
            DocumentVersion.objects.create(
                document=doc,
                version_number=version_number,
                content=doc.content,
                created_by=self.request.user
            )

    def perform_update(self, serializer):
        with transaction.atomic():
            doc = serializer.save()
            version_number = doc.versions.count() + 1
            DocumentVersion.objects.create(
                document=doc,
                version_number=version_number,
                content=doc.content,
                created_by=self.request.user
            )

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        doc = self.get_object()
        versions = doc.versions.all().order_by('-version_number')
        return Response(DocumentVersionSerializer(versions, many=True).data)
        
    @action(detail=True, methods=['get'])
    def tags(self, request, pk=None):
        doc = self.get_object()
        tag_ids = doc.tags.values_list('id', flat=True)
        return Response({"tag_ids": tag_ids})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'document').all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.annotate(document_count=Count('documents')).all()

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('actor').all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
