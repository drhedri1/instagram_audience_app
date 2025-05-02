from flask import Blueprint, jsonify, request, current_app
from src.utils.auth_utils import token_required
from src.models.base import db
from src.models.report import Report
from src.models.audience_data import AudienceData
from datetime import datetime

reports_bp = Blueprint("reports", __name__)

# Placeholder for report generation logic
def generate_audience_report(audience_data):
    """Generates a structured report from audience data."""
    report_content = {
        "summary": {
            "report_date": datetime.utcnow().isoformat(),
            "audience_data_date": audience_data.data_date.isoformat() if audience_data else None,
            "message": "Audience analysis report."
        },
        "demographics": {
            "age_gender": audience_data.age_distribution, # Assuming this contains combined age/gender
            "location": audience_data.top_locations
        },
        "interests": audience_data.interests,
        # Add more sections as needed (e.g., engagement summary)
    }
    return report_content

@reports_bp.route("/", methods=["POST"])
@token_required
def create_report(current_user):
    """Generates and saves a new audience report."""
    # Fetch the latest audience data for the user
    latest_audience = AudienceData.query.filter_by(user_id=current_user.id).order_by(AudienceData.data_date.desc()).first()

    if not latest_audience:
        return jsonify({"error": "No audience data available to generate report."}), 404

    try:
        # Generate the report content
        report_data = generate_audience_report(latest_audience)

        # Create and save the report record
        report_name = f"Audience Report - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        new_report = Report(
            user_id=current_user.id,
            report_name=report_name,
            report_data=report_data,
            generation_date=datetime.utcnow()
        )
        db.session.add(new_report)
        db.session.commit()

        return jsonify({
            "message": "Report generated successfully",
            "report_id": new_report.id,
            "report_name": new_report.report_name
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error generating report: {e}")
        return jsonify({"error": "Failed to generate report"}), 500

@reports_bp.route("/", methods=["GET"])
@token_required
def get_reports(current_user):
    """Returns a list of previously generated reports for the user."""
    reports = Report.query.filter_by(user_id=current_user.id).order_by(Report.generation_date.desc()).all()
    reports_list = [
        {
            "id": r.id,
            "report_name": r.report_name,
            "generation_date": r.generation_date.isoformat()
        }
        for r in reports
    ]
    return jsonify(reports_list), 200

@reports_bp.route("/<int:report_id>", methods=["GET"])
@token_required
def get_report_details(current_user, report_id):
    """Returns the details of a specific report."""
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first()

    if not report:
        return jsonify({"error": "Report not found or access denied."}), 404

    return jsonify({
        "id": report.id,
        "report_name": report.report_name,
        "generation_date": report.generation_date.isoformat(),
        "report_data": report.report_data
    }), 200

