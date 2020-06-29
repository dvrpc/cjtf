import datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Meeting


@receiver(pre_save, sender=Meeting)
def add_or_remove_dates_when_minutes_or_materials_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:  # creation of Meeting
        if instance.minutes:
            instance.minutes_added = datetime.datetime.today()
        if instance.presentation_materials:
            instance.pre_mat_added = datetime.datetime.today()
    else:  # editing of Meeting
        if instance.minutes:
            # if new file uploaded (obj is original, instance is new)
            if obj.minutes != instance.minutes:
                instance.minutes_added = datetime.datetime.today()
        else:
            instance.minutes_added = None

        if instance.presentation_materials:
            # if new file uploaded (obj is original, instance is new)
            if obj.presentation_materials != instance.presentation_materials:
                instance.pre_mat_added = datetime.datetime.today()
        else:
            instance.pre_mat_added = None
