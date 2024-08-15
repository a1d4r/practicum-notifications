import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()
SCHEMA = "notification"


class SchemaBase(Base):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class NotificationContent(SchemaBase):
    __tablename__ = "notification_contents"
    __table_args__ = {"schema": SCHEMA}

    notification_template_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.notification_templates.id", ondelete="CASCADE"),
        nullable=False,
    )
    notification_template = relationship("NotificationTemplate", backref="notification_contents")

    template_variables = Column(JSON, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    user_group_id = Column(UUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Notification(SchemaBase):
    __tablename__ = "notifications"
    __table_args__ = {"schema": SCHEMA}

    content_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f"{SCHEMA}.notification_contents.id", ondelete="CASCADE"),
        nullable=False,
    )
    last_sent_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    content = relationship("NotificationContent", backref="notifications")


class NotificationTemplate(SchemaBase):
    __tablename__ = "notification_templates"
    __table_args__ = {"schema": SCHEMA}

    event_type = Column(String(255), nullable=False)
    template_text = Column(Text, nullable=False)
    channels = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
