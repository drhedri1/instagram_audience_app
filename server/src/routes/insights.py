from flask import Blueprint, jsonify, current_app
from src.utils.auth_utils import token_required
from src.models.audience_data import AudienceData
from datetime import datetime

insights_bp = Blueprint("insights", __name__)

# Placeholder for insights generation logic
def generate_actionable_insights(audience_data):
    """Generates actionable insights based on audience data."""
    insights = []

    if not audience_data:
        return ["No audience data available to generate insights."]

    try:
        # Example Insight 1: Based on top age group
        if audience_data.age_distribution:
            top_age_group = max(audience_data.age_distribution, key=audience_data.age_distribution.get)
            insights.append(f"Your primary audience age group is {top_age_group}. Consider tailoring content visuals and language to resonate with this demographic.")

        # Example Insight 2: Based on gender distribution
        if audience_data.gender_distribution:
            # Assuming gender_distribution is part of age_distribution structure like {"F.18-24": 10, "M.18-24": 15, ...}
            # This needs parsing based on actual API response format
            female_percentage = 0
            male_percentage = 0
            total_audience = sum(audience_data.age_distribution.values()) if audience_data.age_distribution else 0
            if total_audience > 0 and isinstance(audience_data.age_distribution, dict):
                for key, value in audience_data.age_distribution.items():
                    if key.startswith("F."):
                        female_percentage += value
                    elif key.startswith("M."):
                        male_percentage += value
                female_percentage = (female_percentage / total_audience) * 100
                male_percentage = (male_percentage / total_audience) * 100

                if female_percentage > 60:
                    insights.append(f"Your audience is predominantly female ({female_percentage:.1f}%). Focus on content themes and products appealing to women.")
                elif male_percentage > 60:
                    insights.append(f"Your audience is predominantly male ({male_percentage:.1f}%). Focus on content themes and products appealing to men.")
                else:
                    insights.append("Your audience has a relatively balanced gender distribution. Maintain diverse content themes.")

        # Example Insight 3: Based on top location
        if audience_data.top_locations:
             # Assuming top_locations is like {"New York, US": 100, "London, GB": 80, ...}
             if isinstance(audience_data.top_locations, dict):
                 top_location = max(audience_data.top_locations, key=audience_data.top_locations.get)
                 insights.append(f"A significant portion of your audience is located in {top_location}. Consider localizing content or running geo-targeted campaigns.")

        # Add more insights based on interests, engagement times (if available), etc.

        if not insights:
            insights.append("Could not generate specific insights from the available data. Ensure your Instagram account is properly connected and has sufficient audience data.")

    except Exception as e:
        current_app.logger.error(f"Error generating insights: {e}")
        insights.append("An error occurred while generating insights.")

    return insights

@insights_bp.route("/", methods=["GET"])
@token_required
def get_insights(current_user):
    """Generates and returns actionable insights based on the latest audience data."""
    # Fetch the latest audience data for the user
    latest_audience = AudienceData.query.filter_by(user_id=current_user.id).order_by(AudienceData.data_date.desc()).first()

    actionable_insights = generate_actionable_insights(latest_audience)

    return jsonify({"insights": actionable_insights}), 200

