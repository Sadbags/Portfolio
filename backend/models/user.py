import uuid
from database import db
from models.basemodel import BaseModel
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # Encriptado con bcrypt
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    addresses = db.relationship('Address', backref='user', lazy=True)
    appointments = db.relationship('Appointment', back_populates='user', lazy=True)  # esto es lo nuevo
    services = db.relationship('Service', back_populates='user', lazy=True) # esto es lo nuevo


    def __init__(self, email, password, is_admin, first_name="", last_name="", **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin
        self.set_password(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def __str__(self):
        return f"[User] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
			'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'is_admin': self.is_admin,
            'password_hash': self.password_hash,
            'addresses': [address.to_dict() for address in self.addresses],
            'appointments': [appointment.to_dict() for appointment in self.appointments], # esto es lo nuevo
            'services': [service.to_dict() for service in self.services], # esto es lo nuevo
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
		}


# codigo que tenia hasta las 1:03 8 sept
