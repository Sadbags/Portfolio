from flask import request, jsonify, abort, Blueprint
from models.appointment import Appointment
from database import db
from datetime import datetime
from models.user import User

appointments_blueprint = Blueprint('appointments_blueprint', __name__)

@appointments_blueprint.route('/appointments', methods=['POST'])
def create_appointment():
    # Verificar que todos los campos requeridos están en la solicitud
    if not request.json or not 'user_id' in request.json or not 'service_id' in request.json or not 'Appointment_date' in request.json or not 'Appointment_time' in request.json or not 'status' in request.json or not 'payment_status' in request.json:
        abort(400, description="Missing required fields")

    # Obtener datos de la solicitud
    user_id = request.json['user_id']
    service_id = request.json['service_id']
    appointment_date_str = request.json['Appointment_date']
    appointment_time = request.json['Appointment_time']
    status = request.json['status']
    payment_status = request.json['payment_status']

    # Convertir la cadena de Appointment_date a objeto datetime
    try:
        Appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        abort(400, description="Invalid date format. Use YYYY-MM-DDTHH:MM:SS")

    # Crear la instancia de Appointment
    appointment = Appointment(
        user_id=user_id,
        service_id=service_id,
        Appointment_date=Appointment_date,
        Appointment_time=appointment_time,
        status=status,
        payment_status=payment_status
    )

    # Agregar la cita a la sesión de la base de datos y hacer commit
    db.session.add(appointment)
    db.session.commit()

    # Retornar la cita creada en formato JSON
    return jsonify(appointment.to_dict()), 201


@appointments_blueprint.route('/appointments', methods=['GET'])
def get_appointments():
    # Obtener todas las citas de la base de datos
    appointments = Appointment.query.all()

    # Retornar las citas en formato JSON
    return jsonify([appointment.to_dict() for appointment in appointments]), 200


@appointments_blueprint.route('/users/<user_id>/appointments', methods=['GET'])
def get_user_appointments(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return jsonify([appointment.to_dict() for appointment in appointments]), 200


@appointments_blueprint.route('/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    # Buscar la cita existente por su ID
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        abort(404, description="Appointment not found")

    # Retornar la cita en formato JSON
    return jsonify(appointment.to_dict())


@appointments_blueprint.route('/appointments/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    # Verificar que el cuerpo de la solicitud tiene los campos requeridos
    if not request.json:
        abort(400, description="Missing request body")

    # Obtener los datos de la solicitud
    user_id = request.json.get('user_id')
    service_id = request.json.get('service_id')
    appointment_date_str = request.json.get('Appointment_date')
    appointment_time = request.json.get('Appointment_time')
    status = request.json.get('status')
    payment_status = request.json.get('payment_status')

    # Convertir la cadena de Appointment_date a objeto datetime
    try:
        Appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%dT%H:%M:%S') if appointment_date_str else None
    except ValueError:
        abort(400, description="Invalid date format. Use YYYY-MM-DDTHH:MM:SS")

    # Buscar la cita existente por su ID
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        abort(404, description="Appointment not found")

    # Actualizar los campos de la cita
    if user_id:
        appointment.user_id = user_id
    if service_id:
        appointment.service_id = service_id
    if Appointment_date:
        appointment.Appointment_date = Appointment_date
    if appointment_time:
        appointment.Appointment_time = appointment_time
    if status:
        appointment.status = status
    if payment_status:
        appointment.payment_status = payment_status

    # Hacer commit en la base de datos
    db.session.commit()

    # Retornar la cita actualizada en formato JSON
    return jsonify(appointment.to_dict()), 200


@appointments_blueprint.route('/appointments/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    # Buscar la cita existente por su ID
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        abort(404, description="Appointment not found")

    # Eliminar la cita de la base de datos y hacer commit
    db.session.delete(appointment)
    db.session.commit()

    # Retornar un mensaje de confirmación
    return jsonify({"message": "Appointment deleted"}), 200
