from src.models.base import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instagram_user_id = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), nullable=True) # Optional: Store username
    access_token = db.Column(db.String(512), nullable=False) # Store securely (consider encryption)
    # Add other relevant user fields if needed, e.g., profile picture URL, full name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (add later if needed, e.g., one-to-many with AudienceData, Reports)
    # audience_data = db.relationship("AudienceData", backref="user", lazy=True)
    # reports = db.relationship("Report", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.instagram_user_id}>"

