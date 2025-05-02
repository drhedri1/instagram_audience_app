import requests
import os
from flask import current_app

BASE_GRAPH_URL = "https://graph.instagram.com"

def get_instagram_user_info(access_token):
    """Fetches basic user information (ID, username) from Instagram Graph API."""
    url = f"{BASE_GRAPH_URL}/me?fields=id,username&access_token={access_token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching Instagram user info: {e}")
        return None

def get_instagram_audience_insights(instagram_business_account_id, access_token, since_date=None, until_date=None):
    """
    Fetches audience insights (demographics, location) for a given Instagram Business Account.
    Requires instagram_manage_insights permission.
    Note: The Instagram Graph API for insights requires a connected Facebook Page and Instagram Business Account.
    The user_id obtained from basic OAuth might not be the business account ID.
    This function assumes `instagram_business_account_id` is correctly obtained (e.g., via /me/accounts endpoint).
    """
    # Define the metrics we want to fetch
    # Common metrics: audience_gender_age, audience_locale, audience_city, audience_country
    # Check Instagram Graph API documentation for available metrics and required permissions.
    metrics = "audience_gender_age,audience_locale,audience_city,audience_country"
    period = "lifetime" # Insights are often lifetime, but check API docs

    url = f"https://graph.facebook.com/v19.0/{instagram_business_account_id}/insights?metric={metrics}&period={period}&access_token={access_token}"

    # Add date range if provided (Note: Not all lifetime metrics support date ranges)
    # if since_date and until_date:
    #     url += f"&since={since_date.strftime('%Y-%m-%d')}&until={until_date.strftime('%Y-%m-%d')}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Process the insights data into a more usable format
        insights = {}
        for item in data.get("data", []):
            metric_name = item.get("name")
            values = item.get("values", [])
            if values:
                # For lifetime metrics, usually the last value is relevant
                insights[metric_name] = values[-1].get("value")

        return insights

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching Instagram insights: {e} - Response: {response.text if response else 'No response'}")
        # Handle specific errors, e.g., permission errors, account not linked
        if response is not None and response.status_code in [400, 403]:
            error_data = response.json().get("error", {})
            error_message = error_data.get("message", "Permission or configuration error.")
            error_subcode = error_data.get("error_subcode")
            # Specific subcode for insights permission issues
            if error_subcode == 210:
                 return {"error": "Insights permission required or account not eligible.", "details": error_message}
            return {"error": "Failed to fetch insights.", "details": error_message}
        return {"error": "Failed to communicate with Instagram API for insights."}
    except Exception as e:
        current_app.logger.error(f"Unexpected error processing Instagram insights: {e}")
        return {"error": "An internal error occurred while processing insights."}

# Helper function to get the Instagram Business Account ID linked to the user's Facebook Page
# This often requires the pages_show_list permission
def get_instagram_business_account(access_token):
    """Fetches the Instagram Business Account ID linked via a Facebook Page."""
    # First, get the user's Facebook Pages
    pages_url = f"https://graph.facebook.com/v19.0/me/accounts?fields=id,name,access_token,instagram_business_account{{id,username}}&access_token={access_token}"
    try:
        pages_response = requests.get(pages_url)
        pages_response.raise_for_status()
        pages_data = pages_response.json()

        # Find the first page with a linked Instagram Business Account
        for page in pages_data.get("data", []):
            if "instagram_business_account" in page:
                ig_account_id = page["instagram_business_account"]["id"]
                # Optionally, get a page-specific access token if needed for insights
                # page_access_token = page.get("access_token")
                return ig_account_id

        return None # No linked Instagram Business Account found

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching Facebook pages/linked Instagram account: {e} - Response: {pages_response.text if pages_response else 'No response'}")
        if pages_response is not None and pages_response.status_code in [400, 403]:
             error_data = pages_response.json().get("error", {})
             return {"error": "Failed to fetch linked accounts.", "details": error_data.get("message")}
        return {"error": "Failed to communicate with Facebook API."}
    except Exception as e:
        current_app.logger.error(f"Unexpected error getting Instagram Business Account: {e}")
        return {"error": "An internal error occurred while finding the business account."}


