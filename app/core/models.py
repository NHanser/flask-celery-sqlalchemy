
from flask_security import MailUtil

class MyMailUtil(MailUtil):
    def send_mail(self, template, subject, recipient, sender, body, html, user, **kwargs):
        from app.core.tasks import send_flask_mail
        send_flask_mail.delay(
            subject=subject,
            sender=sender,
            recipients=[recipient],
            body=body,
            html=html,
        )