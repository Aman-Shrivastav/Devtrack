from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, WorkspaceViewSet, WorkspaceMemberViewSet,
                    DocumentViewSet, CommentViewSet, TagViewSet, AuditLogViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')
router.register(r'workspace-members', WorkspaceMemberViewSet, basename='workspace-member')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
]
