from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver


@receiver(pre_delete, sender=User)
def pre_delete_user(sender, **kwargs):
    if kwargs['instance'].is_superuser and len(User.objects.filter(is_superuser=True)) == 1:
        raise Exception('Nie możesz usunąć ostatniego admina')
