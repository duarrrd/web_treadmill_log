from flask import render_template, jsonify, request
from app import app, db
from datetime import datetime
from app.models import Diameter, Session, Record


@app.route('/')
def main():
    sessions = Session.query.all()
    return render_template('main.html', sessions=sessions)



@app.route('/activity', methods=['POST'])
def activity():
    data = request.get_json()
    device_id = data['device_id']
    start_time = datetime.fromisoformat(data['start_time'])

    diameter = Diameter.query.get(device_id)

    if not diameter:
        return jsonify({'error': 'Device not found'}), 404

    session = Session()
    session.device_id = device_id
    session.start_time = start_time

    db.session.add(session)
    db.session.commit()

    record = Record()
    record.session_id = session.session_id
    record.start_time = start_time

    db.session.add(record)
    db.session.commit()

    return jsonify({'session_id': session.session_id})

@app.route('/activity/<int:session_id>', methods=['PUT'])
def update_activity(session_id):
    data = request.get_json()
    end_time = datetime.fromisoformat(data['end_time'])
    sensor_triggers = data['sensor_triggers']

    record = Record.query.filter_by(session_id=session_id).order_by(Record.start_time.desc()).first()

    if not record:
        return jsonify({'error': 'Record not found'}), 404

    record.end_time = end_time
    record.sensor_triggers = sensor_triggers
    db.session.commit()

    return jsonify({'message': 'Record updated'})

@app.route('/activity/<int:session_id>/end', methods=['PUT'])
def end_activity(session_id):
    session = Session.query.get(session_id)

    if not session:
        return jsonify({'error': 'Session not found'}), 404

    data = request.get_json()
    end_time = datetime.fromisoformat(data['end_time'])

    session.end_time = end_time
    session.duration = (session.end_time - session.start_time).total_seconds()

    diameter = session.diameter.diameter
    sensor_triggers = sum(record.sensor_triggers for record in session.records if record.sensor_triggers is not None)
    session.distance = (sensor_triggers * diameter * 3.14159) / 1000
    session.speed = (session.distance / session.duration) * 3.6

    db.session.commit()

    return jsonify({'message': 'Session ended'})