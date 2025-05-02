from src.models.base import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    report_name = db.Column(db.String(255), nullable=False)
    report_data = db.Column(db.JSON, nullable=False) # Store generated report content (e.g., summary, charts data)
    generation_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Add other relevant report fields if needed, e.g., report type, parameters used

    user = db.relationship("User", backref=db.backref("reports", lazy=True))

    def __repr__(self):
        return f"<Report {self.report_name} for User {self.user_id}>"

