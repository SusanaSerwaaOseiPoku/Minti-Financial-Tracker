from flask import Flask, request, jsonify
from minti_logic import MintiLogic

app = Flask(__name__)

# instantiate the app logic
minti_app = MintiLogic()


@app.route("/api/summary", methods=["GET"])
def get_summary():
    """Returns the current month's summary and feedback"""
    try:
        year_month = request.args.get("month")
        summary = minti_app.get_monthly_summary(year_month) if year_month else minti_app.get_monthly_summary()
        spending = None
        if isinstance(summary, dict):
            spending = summary.get("current_spending") or summary.get("current spending") or summary.get("spending") or 0
        else:
            spending = 0
        feedback_func = getattr(minti_app, "generate_feedback", None) or getattr(minti_app, "generated_feedback", None)
        feedback = feedback_func(spending) if feedback_func else None
        response_data = {
            "summary": summary,
            "feedback": feedback,
            "budget": getattr(minti_app, "MONTHLY_BUDGET", None)
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/transaction", methods=["POST"])
def record_transaction():
    """Receives transaction data from frontend and saves it"""
    transaction_data = request.get_json()
    if not transaction_data:
        return jsonify({"message": "No data provided"}), 400
    success = False
    try:
        success = minti_app.data_manager.record_transaction(transaction_data)
    except Exception as e:
        return jsonify({"message": "Failed to record transaction", "error": str(e)}), 500
    if success:
        return jsonify({"message": "Transaction recorded successfully"}), 201
    return jsonify({"message": "Failed to record transaction"}), 500


if __name__ == "__main__":
    print("Start Flask server")
    app.run(debug=True)
