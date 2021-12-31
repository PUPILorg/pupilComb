from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.core.files.storage import default_storage

@receiver(post_delete, sender='base.Media')
def delete_from_s3(sender, instance, **kwargs):
    print(instance.file.name)
    default_storage.delete(instance.file.name)
