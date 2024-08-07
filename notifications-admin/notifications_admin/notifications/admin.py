from django.contrib import admin

from .models import Notifications, NotificationsContents, NotificationsTemplates


class NotificationsInline(admin.TabularInline):
    model = Notifications


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('content_id', 'last_sent_at',)


@admin.register(NotificationsContents)
class NotificationsContentsAdmin(admin.ModelAdmin):
    inlines = (NotificationsInline,)
    list_display = ('event_type', 'user_id', 'user_group_id',)


@admin.register(NotificationsTemplates)
class NotificationsTemplatesAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'channels',)
    list_filter = ('channels',)
