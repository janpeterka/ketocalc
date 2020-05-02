import datetime

from app import db

from app.models.users import User


class SentMail(db.Model):
    __tablename__ = "sent_mails"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    subject = db.Column(db.String(255), nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    recipient_id = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    bcc = db.Column(db.String(255), nullable=True)
    template = db.Column(db.Text(), nullable=True)

    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    recipient = db.relationship("User", uselist=False, back_populates="sent_mails")

    def fill_from_message(self, message, recipient):
        self.subject = message.subject
        self.sender = message.sender
        self.recipient_id = User.load(message.recipient, load_type="username").id
        self.bcc = str(message.bcc)
        self.template = message.template
