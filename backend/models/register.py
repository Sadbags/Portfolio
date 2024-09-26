import uuid
from backend.database import db
from backend.models.basemodel import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Register(BaseModel):
    __tablename__ = 'registered'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # Encriptado con bcrypt
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    street = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

    appointments = db.relationship('Appointment', back_populates='register', lazy=True)  # esto es lo nuevo
    services = db.relationship('Service', back_populates='register', lazy=True)

    def __init__(self, email, password, is_admin, user_type, first_name="", last_name="", street="", city="", phone="", state="", zip_code="", **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin
        self.address = address
        self.street = street
        self.city = city
        self.phone = phone
        self.state = state
        self.zip_code = zip_code
        self.set_password(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def __str__(self):
        return f"[Register] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'is_admin': self.is_admin,
            'user_type': self.user_type,
            'address': self.address,
            'password_hash': self.password_hash,
            'appointments': [appointment.to_dict() for appointment in self.appointments], # esto es lo nuevo
            'services': [service.to_dict() for service in self.services], # esto es lo nuevo
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
