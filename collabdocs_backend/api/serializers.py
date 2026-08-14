from rest_framework import serializers
from .models import User, Workspace, WorkspaceMember, Document, DocumentVersion, Comment, Tag, AuditLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class WorkspaceSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'description', 'owner', 'is_active', 'member_count', 'created_at']
        read_only_fields = ['owner']

    def get_member_count(self, obj):
        return obj.members.count()

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Workspace name must be at least 3 characters long.")
        return value

class WorkspaceMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceMember
        fields = ['id', 'workspace', 'user', 'role', 'joined_at']

class DocumentSerializer(serializers.ModelSerializer):
    version_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'workspace', 'created_by', 'status', 'version_count', 'created_at', 'updated_at']
        read_only_fields = ['created_by']

    def get_version_count(self, obj):
        return obj.versions.count()

    def validate(self, data):
        if data.get('status') == Document.StatusChoices.PUBLISHED and not data.get('content'):
            raise serializers.ValidationError("Cannot publish an empty document.")
        return data

class DocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author']

class TagSerializer(serializers.ModelSerializer):
    document_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'document_count']

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
