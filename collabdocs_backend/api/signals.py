from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document, AuditLog

@receiver(post_save, sender=Document)
def create_audit_log(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    
    if kwargs.get('raw', False):
        return

    AuditLog.objects.create(
        action=action,
        actor=instance.created_by,
        model_name='Document',
        object_id=instance.id
    )
