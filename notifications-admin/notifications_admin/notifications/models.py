from typing import Any

import uuid

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from jinja2 import Environment, TemplateSyntaxError


def jinja_validator(value: str) -> None:
    try:
        Environment().parse(value)
    except TemplateSyntaxError as err:
        raise ValidationError(_("Template syntax error: %s") % err) from None


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class NotificationsTemplates(UUIDMixin, TimeStampedMixin):
    class Channel(models.TextChoices):
        SMS = "sms", _("SMS")
        EMAIL = "email", _("Email")
        WEBSOCKET = "websocket", _("WebSocket")

    event_type = models.CharField(_("event type"), max_length=255, unique=True)
    template_text = models.TextField(_("Template"), validators=[jinja_validator])
    channels = ArrayField(
        models.CharField(choices=Channel.choices, max_length=255, verbose_name=_("channels")),
        blank=True,
        default=list,
    )

    class Meta:
        db_table = 'notification"."notification_templates'
        indexes = [models.Index(fields=["event_type"], name="event_type_idx")]
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self) -> Any:
        return self.event_type


class NotificationsContents(UUIDMixin, TimeStampedMixin):
    event_type = models.ForeignKey(
        NotificationsTemplates, on_delete=models.CASCADE, verbose_name=_("event type")
    )
    template_variables = models.JSONField(verbose_name=_("Template Variables"), default={})
    user_id = models.UUIDField(null=True, verbose_name=_("User ID"))
    user_group_id = models.UUIDField(null=True, verbose_name=_("Group ID"))

    class Meta:
        db_table = 'notification"."notification_contents'
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")

    def __str__(self) -> Any:
        return f"Notification content for {self.event_type}"


class Notifications(UUIDMixin):
    content_id = models.ForeignKey(
        NotificationsContents, on_delete=models.CASCADE, verbose_name=_("content id")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    last_sent_at = models.DateTimeField(verbose_name=_("last sent at"))

    class Meta:
        db_table = 'notification"."notifications'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self) -> Any:
        return f"Notification {self.last_sent_at}"
