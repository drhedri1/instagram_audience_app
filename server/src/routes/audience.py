from flask import Blueprint, jsonify, current_app
from src.utils.auth_utils import token_required
from src.services.instagram_service import get_instagram_business_account, get_instagram_audience_insights
from src.models.base import db
from src.models.audience_data import AudienceData
from datetime import datetime

audience_bp = Blueprint("audience", __name__)

@audience_bp.route("/", methods=["GET"])
@token_required
def get_audience_data(current_user):
    """Fetches audience insights from Instagram Graph API and returns them."""
    access_token = current_user.access_token

    # 1. Get the Instagram Business Account ID
    ig_business_account_id_result = get_instagram_business_account(access_token)

    if isinstance(ig_business_account_id_result, dict) and "error" in ig_business_account_id_result:
        # Handle error fetching business account ID
        return jsonify(ig_business_account_id_result), 400 # Or 500/502 depending on error

    if not ig_business_account_id_result:
        return jsonify({"error": "No linked Instagram Business Account found or accessible."}), 404

    ig_business_account_id = ig_business_account_id_result

    # 2. Fetch Insights using the Business Account ID
    insights_data = get_instagram_audience_insights(ig_business_account_id, access_token)

    if isinstance(insights_data, dict) and "error" in insights_data:
        # Handle error fetching insights
        return jsonify(insights_data), 400 # Or 500/502 depending on error

    # 3. (Optional) Store fetched insights in the database
    try:
        # Check if data for today already exists
        today_date = datetime.utcnow().date()
        existing_data = AudienceData.query.filter_by(user_id=current_user.id, data_date=today_date).first()

        # Process raw insights into model fields (example)
        processed_data = {
            "age_distribution": insights_data.get("audience_gender_age"),
            "gender_distribution": insights_data.get("audience_gender_age"), # Often combined, needs parsing
            "top_locations": insights_data.get("audience_city") or insights_data.get("audience_country"), # Combine/prioritize
            # Add other fields like reach, impressions if fetched
        }

        if existing_data:
            # Update existing record for today
            for key, value in processed_data.items():
                setattr(existing_data, key, value)
            current_app.logger.info(f"Updated audience data for user {current_user.id} on {today_date}")
        else:
            # Create new record
            new_audience_data = AudienceData(
                user_id=current_user.id,
                data_date=today_date,
                **processed_data
            )
            db.session.add(new_audience_data)
            current_app.logger.info(f"Created new audience data for user {current_user.id} on {today_date}")

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving audience data to DB: {e}")
        # Decide if this should be a fatal error or just log and continue
        # return jsonify({"error": "Failed to save audience data"}), 500

    # 4. Return the fetched (and potentially processed) insights
    # Return the raw insights or the processed data based on frontend needs
    return jsonify(insights_data), 200

