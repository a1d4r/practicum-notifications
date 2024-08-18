from typing import Any

import datetime
import uuid

from sqlalchemy import (
    ARRAY,
    DateTime,
    ForeignKeyConstraint,
    Index,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="notification_templates_pkey"),
        UniqueConstraint("event_type", name="notification_templates_event_type_key"),
        Index("event_type_idx", "event_type"),
        Index("notification_templates_event_type_92865815_like", "event_type"),
        {"schema": "notification"},
    )

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(255))
    template_text: Mapped[str] = mapped_column(Text)
    channels: Mapped[list[str]] = mapped_column(ARRAY(String(length=255)))


class NotificationContent(Base):
    __tablename__ = "notification_contents"
    __table_args__ = (
        ForeignKeyConstraint(
            ["event_type_id"],
            ["notification.notification_templates.id"],
            deferrable=True,
            initially="DEFERRED",
            name="notification_content_event_type_id_9fd2cd36_fk_notificat",
        ),
        PrimaryKeyConstraint("id", name="notification_contents_pkey"),
        Index("notification_contents_event_type_id_9fd2cd36", "event_type_id"),
        {"schema": "notification"},
    )

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    template_variables: Mapped[dict[str, Any]] = mapped_column(JSONB)
    event_type_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    user_id: Mapped[uuid.UUID | None] = mapped_column(Uuid)
    user_group_id: Mapped[uuid.UUID | None] = mapped_column(Uuid)

    template: Mapped[NotificationTemplate] = relationship("NotificationTemplate", lazy="joined")


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        ForeignKeyConstraint(
            ["content_id"],
            ["notification.notification_contents.id"],
            deferrable=True,
            initially="DEFERRED",
            name="notifications_content_id_a84315b7_fk_notificat",
        ),
        PrimaryKeyConstraint("id", name="notifications_pkey"),
        Index("notifications_content_id_a84315b7", "content_id"),
        {"schema": "notification"},
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    last_sent_at: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    content_id: Mapped[uuid.UUID] = mapped_column(Uuid)

    content: Mapped[NotificationContent] = relationship("NotificationContent", lazy="joined")
