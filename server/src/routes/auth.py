import os
import requests
from flask import Blueprint, request, jsonify, redirect, url_for, current_app, make_response
from src.models.base import db
from src.models.user import User
from src.utils.auth_utils import generate_token, token_required # Import token_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/instagram/login")
def instagram_login():
    """Redirects the user to Instagram for authorization."""
    # Ensure these are set in your .env file
    app_id = os.getenv("INSTAGRAM_APP_ID")
    redirect_uri = os.getenv("INSTAGRAM_REDIRECT_URI")

    if not app_id or not redirect_uri:
        return jsonify({"error": "Instagram App ID or Redirect URI not configured."}), 500

    # Scopes required for audience insights (adjust as needed based on Graph API docs)
    # Common scopes: instagram_basic, instagram_manage_insights, pages_show_list, pages_read_engagement
    scopes = "instagram_basic,instagram_manage_insights,pages_show_list,pages_read_engagement"

    # Construct the Instagram authorization URL
    auth_url = f"https://api.instagram.com/oauth/authorize?client_id={app_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code"

    return redirect(auth_url)

@auth_bp.route("/instagram/callback")
def instagram_callback():
    """Handles the callback from Instagram after authorization."""
    code = request.args.get("code")
    error = request.args.get("error")
    error_reason = request.args.get("error_reason")
    error_description = request.args.get("error_description")

    if error:
        current_app.logger.error(f"Instagram OAuth Error: {error} - {error_reason} - {error_description}")
        # Redirect to a frontend error page or show an error message
        # For now, return JSON error
        return jsonify({"error": "Authorization failed", "details": error_description}), 400

    if not code:
        return jsonify({"error": "Authorization code missing"}), 400

    # Exchange the code for a short-lived access token
    app_id = os.getenv("INSTAGRAM_APP_ID")
    app_secret = os.getenv("INSTAGRAM_APP_SECRET")
    redirect_uri = os.getenv("INSTAGRAM_REDIRECT_URI")

    if not app_id or not app_secret or not redirect_uri:
        return jsonify({"error": "Instagram App credentials or Redirect URI not configured."}), 500

    token_url = "https://api.instagram.com/oauth/access_token"
    payload = {
        "client_id": app_id,
        "client_secret": app_secret,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "code": code,
    }

    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        short_lived_token = data.get("access_token")
        instagram_user_id = data.get("user_id")

        if not short_lived_token or not instagram_user_id:
            current_app.logger.error(f"Failed to get access token or user ID: {data}")
            return jsonify({"error": "Failed to obtain access token from Instagram"}), 500

        # OPTIONAL: Exchange short-lived token for a long-lived token
        # This is recommended for better user experience
        long_lived_token_url = f"https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={app_secret}&access_token={short_lived_token}"
        long_lived_response = requests.get(long_lived_token_url)
        long_lived_response.raise_for_status()
        long_lived_data = long_lived_response.json()
        access_token = long_lived_data.get("access_token", short_lived_token) # Use long-lived if available

        # --- User Handling ---
        # Check if user exists, otherwise create a new one
        user = User.query.filter_by(instagram_user_id=str(instagram_user_id)).first()

        if user:
            # Update existing user's token (important for token refresh)
            user.access_token = access_token
            db.session.commit()
            current_app.logger.info(f"Updated token for existing user: {instagram_user_id}")
        else:
            # Create new user
            # Optionally fetch username or other details here using the access_token
            new_user = User(instagram_user_id=str(instagram_user_id), access_token=access_token)
            db.session.add(new_user)
            db.session.commit()
            user = new_user # Use the newly created user object
            current_app.logger.info(f"Created new user: {instagram_user_id}")

        # --- Session/Token Generation ---
        # Generate your application's JWT token
        app_token = generate_token(user.id)

        # Redirect user to the frontend dashboard, passing the token
        # Option 1: Redirect with token in query param (less secure)
        # frontend_url = f"http://localhost:3000/dashboard?token={app_token}" # Adjust frontend URL

        # Option 2: Set token in a secure HTTPOnly cookie
        frontend_dashboard_url = "/dashboard" # Relative URL for the frontend route
        response = make_response(redirect(frontend_dashboard_url))
        # Set cookie parameters appropriately for security (HttpOnly, Secure in production, SameSite)
        response.set_cookie(
            'auth_token',
            app_token,
            httponly=True,
            secure=request.is_secure, # Set to True in production (HTTPS)
            samesite='Lax' # Or 'Strict'
            # max_age=... # Optional: Set cookie expiry
        )
        return response

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error exchanging code for token: {e}")
        return jsonify({"error": "Failed to communicate with Instagram API"}), 502 # Bad Gateway
    except Exception as e:
        current_app.logger.error(f"Error during callback processing: {e}")
        db.session.rollback() # Rollback db changes on error
        return jsonify({"error": "An internal error occurred"}), 500

@auth_bp.route("/check")
@token_required
def check_auth(current_user):
    """An endpoint to check if the user's token is valid."""
    # The token_required decorator handles validation.
    # If we reach here, the token is valid.
    # Optionally return user info
    return jsonify({
        "message": "Token is valid",
        "user_id": current_user.id,
        "instagram_user_id": current_user.instagram_user_id
    }), 200

@auth_bp.route("/logout")
def logout():
    """Logs the user out by clearing the auth cookie."""
    # Redirect to login page or home page after clearing cookie
    response = make_response(redirect("/")) # Adjust redirect target as needed
    response.set_cookie('auth_token', '', expires=0, httponly=True, secure=request.is_secure, samesite='Lax')
    return response

