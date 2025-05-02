from src.models.base import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    target_demographics = db.Column(db.JSON, nullable=True) # e.g., {"age_range": ["18-34"], "gender": ["female"], "locations": ["USA", "Canada"]}
    target_interests = db.Column(db.JSON, nullable=True) # e.g., ["Fashion", "Beauty", "Skincare"]
    image_url = db.Column(db.String(512), nullable=True)
    product_url = db.Column(db.String(512), nullable=True)
    # Add other relevant product fields if needed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.name}>"

