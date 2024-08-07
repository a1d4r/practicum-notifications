import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class NotificationsContents(UUIDMixin, TimeStampedMixin):
    event_type = models.CharField(_('event type'), max_length=255)
    template_variables = models.JSONField(verbose_name=_('Template Variables'))
    user_id = models.UUIDField(verbose_name=_('User ID'))
    user_group_id = models.UUIDField(verbose_name=_('Group ID'))

    class Meta:
        db_table = 'notification\".\"notification_contents'
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')


class NotificationsTemplates(UUIDMixin, TimeStampedMixin):
    class Channel(models.TextChoices):
        DIRECTOR = 'sms', _('SMS')
        WRITER = 'email', _('Email')
        ACTOR = 'websocket', _('WebSocket')

    event_type = models.CharField(_('event type'), max_length=255)
    template_text = models.TextField(_('Template'))
    channels = models.CharField(
        choices=Channel.choices,
        max_length=255,
        verbose_name=_('channels')
    )

    class Meta:
        db_table = 'notification\".\"notification_templates'
        indexes = [
            models.Index(fields=['event_type'], name='event_type_idx'),
        ]
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')


class Notifications(UUIDMixin):
    content_id = models.ForeignKey(NotificationsContents, on_delete=models.CASCADE, verbose_name=_('content id'))
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(auto_now=True, verbose_name=_('last sent at'))

    class Meta:
        db_table = 'notification\".\"notifications'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
