from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from users.models import Autor, Profile, Reader, User


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            email=user.email,
            username=user.username,
            name=f"{user.first_name} {user.last_name}",
        )

    print("Profile saved")


@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()

    print("Delitig user ...")
