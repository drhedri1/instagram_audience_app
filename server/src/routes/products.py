from flask import Blueprint, jsonify, request
from src.utils.auth_utils import token_required
from src.models.product import Product
from src.models.audience_data import AudienceData
from datetime import datetime

products_bp = Blueprint("products", __name__)

# Placeholder for product matching logic
def match_products_to_audience(audience_data, products):
    """Matches products to audience based on demographics and interests."""
    matched_products = []
    # Basic example: Match if product target age overlaps with top audience age
    # This needs significant refinement based on actual data structure and matching criteria
    try:
        top_audience_age = max(audience_data.get("age_distribution", {}), key=audience_data.get("age_distribution", {}).get) if audience_data.get("age_distribution") else None

        for product in products:
            target_ages = product.target_demographics.get("age_range", []) if product.target_demographics else []
            # Very simple overlap check
            if top_audience_age and any(age_range == top_audience_age for age_range in target_ages):
                 matched_products.append(product)
            # Add more sophisticated matching based on gender, location, interests etc.

        # If no specific matches, maybe return all products or a default set
        if not matched_products:
             return products[:5] # Return first 5 as fallback

        return matched_products

    except Exception as e:
        # Log error
        print(f"Error during product matching: {e}")
        return products[:5] # Fallback

@products_bp.route("/", methods=["GET"])
@token_required
def get_products(current_user):
    """Returns a list of products, potentially filtered or matched to the user's audience."""
    # Fetch all products from DB (consider pagination for large datasets)
    products = Product.query.all()

    # Fetch latest audience data for the user
    latest_audience = AudienceData.query.filter_by(user_id=current_user.id).order_by(AudienceData.data_date.desc()).first()

    matched_products_list = []
    if latest_audience:
        # Convert audience data model to dict-like structure if needed for matching function
        audience_dict = {
            "age_distribution": latest_audience.age_distribution,
            "gender_distribution": latest_audience.gender_distribution,
            "top_locations": latest_audience.top_locations,
            "interests": latest_audience.interests
        }
        matched_products = match_products_to_audience(audience_dict, products)
        matched_products_list = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "image_url": p.image_url,
                "product_url": p.product_url
                # Add other fields as needed
            }
            for p in matched_products
        ]
    else:
        # Fallback if no audience data exists - return all products or a subset
        matched_products_list = [
             {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "image_url": p.image_url,
                "product_url": p.product_url
            }
            for p in products[:10] # Example: return first 10
        ]

    return jsonify(matched_products_list), 200

# Optional: Add routes for adding/managing products if needed
# @products_bp.route("/", methods=["POST"])
# @token_required
# def add_product(current_user):
#     # ... implementation ...
#     pass

