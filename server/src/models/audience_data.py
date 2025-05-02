from src.models.base import db
from datetime import datetime

class AudienceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Demographics
    age_distribution = db.Column(db.JSON, nullable=True) # e.g., {"18-24": 40, "25-34": 30, ...}
    gender_distribution = db.Column(db.JSON, nullable=True) # e.g., {"male": 45, "female": 55}
    top_locations = db.Column(db.JSON, nullable=True) # e.g., [{"city": "New York", "country": "USA", "percentage": 20}, ...]
    # Interests (Could be complex, JSON might be suitable)
    interests = db.Column(db.JSON, nullable=True) # e.g., ["Fashion", "Travel", "Food", ...]
    # Engagement Metrics
    reach = db.Column(db.Integer, nullable=True)
    impressions = db.Column(db.Integer, nullable=True)
    profile_views = db.Column(db.Integer, nullable=True)
    # Timestamps
    data_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("audience_data", lazy=True))

    def __repr__(self):
        return f"<AudienceData for User {self.user_id} on {self.data_date}>"

