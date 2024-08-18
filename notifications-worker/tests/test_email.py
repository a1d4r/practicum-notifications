from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from email.message import EmailMessage


async def test_send_email_with_text_and_html(test_broker, smtp_client_mock):
    # Arrange
    recipient = "test@example.com"
    subject = "Greetings"
    text = "Hello, John Doe!"
    html = "<p>Hello, John Doe!</p>"

    # Act
    await test_broker.publish(
        {"email": recipient, "subject": subject, "text": text, "html": html},
        queue="notifications_email",
    )

    # Assert
    assert smtp_client_mock.send_message.call_count == 1
    message: EmailMessage = smtp_client_mock.send_message.call_args[0][0]
    message_parts = list(message.iter_parts())
    assert message.get("To") == recipient
    assert message.get("Subject") == subject
    assert message_parts[0].get_payload().rstrip() == text  # type: ignore[union-attr]
    assert message_parts[1].get_payload().rstrip() == html  # type: ignore[union-attr]
