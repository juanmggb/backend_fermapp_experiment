from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save, post_save
import os
from django.core.files.storage import default_storage
from django.core.files import File
from users.models import User


@receiver(pre_save, sender=User)
def set_default_user_image(sender, instance, **kwargs):
    # Assign default image to user if he has no image
    if not instance.image:
        print("Adding image...")
        default_image_path = "images/default/user-default.jpg"
        default_image = default_storage.open(default_image_path)
        instance.image.save("user-default.png", File(default_image), save=False)


@receiver(pre_delete, sender=User)
def delete_member_image(sender, instance, **kwargs):
    # Delete user
    if instance.image:
        print("Deleting image...")
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=User)
def delete_previous_user_image(sender, instance, **kwargs):
    # Get the user instance before updating
    if instance.pk:
        previous_member = User.objects.get(pk=instance.pk)
        # Delete member's image
        if previous_member.image and previous_member.image != instance.image:
            if os.path.isfile(previous_member.image.path):
                os.remove(previous_member.image.path)
