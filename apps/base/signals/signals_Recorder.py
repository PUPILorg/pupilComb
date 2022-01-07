from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='base.Recorder')
def set_queue(sender, instance, created, **kwargs):
    if created:
        instance.queue_name = f"recorder_{instance.id}"
        instance.save()