from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save, post_save
import os
from django.core.files.storage import default_storage
from django.core.files import File
from .models import Member
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
    if created:
        print("Creating member...")
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_member(sender, instance, **kwargs):
    try:
        print("Saving member...")
        instance.member.save()
    except:
        print("Creating member...")
        Member.objects.create(user=instance)


@receiver(pre_save, sender=Member)
def set_default_memeber_image(sender, instance, **kwargs):
    # Assign default image to member if he has no image
    if not instance.image:
        print("Adding image...")
        default_image_path = "images/default/user-default.jpg"
        default_image = default_storage.open(default_image_path)
        instance.image.save("user-default.png", File(default_image), save=False)


@receiver(pre_delete, sender=Member)
def delete_member_image(sender, instance, **kwargs):
    # Delete member
    if instance.image:
        print("Deleting image...")
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Member)
def delete_previous_member_image(sender, instance, **kwargs):
    # Get the member instance before updating
    if instance.pk:
        previous_member = Member.objects.get(pk=instance.pk)
        # Delete member's image
        if previous_member.image and previous_member.image != instance.image:
            if os.path.isfile(previous_member.image.path):
                os.remove(previous_member.image.path)
