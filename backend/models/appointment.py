from backend.models.basemodel import BaseModel
from backend.database import db
from backend.models.user import User

#CODIGO VIEJO 2:34AM

class Appointment(BaseModel):
    __tablename__ = 'appointments'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.String(128), nullable=False)
    Appointment_date = db.Column(db.DateTime, nullable=False)
    Appointment_time = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)
    payment_status = db.Column(db.String(128), nullable=False)

    user = db.relationship('User', back_populates='appointments')  # esto es lo nuevo

    def __init__(self, user_id, service_id, Appointment_date, Appointment_time, status, payment_status, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.service_id = service_id
        self.Appointment_date = Appointment_date
        self.Appointment_time = Appointment_time
        self.status = status
        self.payment_status = payment_status


    def __str__(self):
        return f"[Appointment] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
			'id': self.id,
			'user_id': self.user_id,
			'service_id': self.service_id,
			'Appointment_date': self.Appointment_date,
			'Appointment_time': self.Appointment_time,
			'status': self.status,
			'payment_status': self.payment_status,
			'created_at': self.created_at.isoformat(),
			'updated_at': self.updated_at.isoformat()
		}
