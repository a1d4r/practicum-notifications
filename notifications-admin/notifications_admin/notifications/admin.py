from typing import Any

from django import forms
from django.contrib import admin
from django.http import HttpRequest

from .models import Notifications, NotificationsContents, NotificationsTemplates


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_change_permission(self, request: HttpRequest, obj: Notifications | None = None) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Notifications | None = None) -> bool:
        return False


class NotificationsInline(admin.TabularInline):
    model = Notifications


class NotificationsTemplatesAdminForm(forms.ModelForm):
    channels = forms.MultipleChoiceField(
        choices=NotificationsTemplates.Channel.choices, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = NotificationsTemplates
        fields = ("event_type", "template_text", "channels")

    def clean_status(self) -> Any:
        return self.cleaned_data.get("channels", [])


@admin.register(Notifications)
class NotificationsAdmin(ReadOnlyAdmin):
    list_display = ("content_id", "created_at", "last_sent_at")


@admin.register(NotificationsContents)
class NotificationsContentsAdmin(admin.ModelAdmin):
    inlines = (NotificationsInline,)
    list_display = ("id", "event_type", "user_id", "user_group_id")


@admin.register(NotificationsTemplates)
class NotificationsTemplatesAdmin(admin.ModelAdmin):
    form = NotificationsTemplatesAdminForm
    list_display = ("event_type", "channels")
    list_filter = ("event_type",)
