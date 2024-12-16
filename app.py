from flask import Flask, jsonify, request
from flask_cors import CORS
from DatabaseManager import DatabaseManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize DatabaseManager
db_manager = DatabaseManager()

@app.route('/incidents', methods=['GET'])
def get_incidents():
    try:
        sort_by = request.args.get('sort', 'severity')  # Default sort by severity
        if sort_by == 'severity':
            incidents = db_manager.get_ordered_by_severity()
        else:
            incidents = db_manager.get_ordered_by_time()
        return jsonify(incidents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/incidents', methods=['POST'])
def add_incident():
    try:
        incident_data = request.json
        db_manager.insert_incident(incident_data)
        return jsonify({"message": "Incident added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/incidents/flagged', methods=['GET'])
def get_flagged_incidents():
    try:
        flagged_incidents = db_manager.get_incidents_by_feature("needs_review")
        return jsonify(flagged_incidents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/incidents/resolved', methods=['GET'])
def get_resolved_incidents():
    try:
        resolved_incidents = db_manager.get_incidents_by_feature("flagged")
        return jsonify(resolved_incidents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/resolve/<string:incident_id>', methods=['POST'])
def resolve_incident(incident_id):
    try:
        db_manager.resolve_incident(incident_id)
        return '', 204  # Return no content with a 204 status code on success
    except Exception as e:
        app.logger.error(f"Error resolving incident: {str(e)}")
        return '', 500  # Return no content with a 500 status code on error

if __name__ == '__main__':
    app.run(debug=True)