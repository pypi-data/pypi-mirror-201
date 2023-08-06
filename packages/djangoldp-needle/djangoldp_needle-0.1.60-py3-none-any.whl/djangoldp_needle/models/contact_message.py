from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.template import loader
from djangoldp.models import Model
from django.db.models.signals import post_save


class ContactMessage(Model):
    target = models.ForeignKey(settings.AUTH_USER_MODEL,
                   related_name='contact_messages',
                   on_delete=models.CASCADE,
           )
    source = models.ForeignKey(settings.AUTH_USER_MODEL,
           related_name='contact_messages_source',
           on_delete=models.CASCADE,
       )
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta(Model.Meta):
        rdf_type = 'hd:contact_message'
        owner_field = 'target'
        owner_perms = ['view', 'add']


@receiver(post_save, sender=ContactMessage)
def post_save_user(sender, instance, created, **kwargs):
    if not created:
        return

    email_from = getattr(settings, 'DEFAULT_FROM_EMAIL', False)
    if not email_from:
        return

    message = loader.render_to_string(
        'email.txt',
        {
            'source': instance.source.email,
            'message': instance.message
        }
    )

    send_mail(
        'Nouveau message de Needle',
        message,
        email_from,
        [instance.target.email],
    )
