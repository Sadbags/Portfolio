from backend.database import db
from backend.models.basemodel import BaseModel
import uuid
import base64
import os


class Service(BaseModel):
    __tablename__ = 'services'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    aprox_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(128), nullable=False)
    fee = db.Column(db.Float, nullable=False)
    picture = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='services')
    reviews = db.relationship('Review', back_populates='service')  # Esto es lo nuevo
    appointments = db.relationship('Appointment', back_populates='service', lazy=True)  # Esto es lo nuevo

    def __init__(self, name, description, aprox_price, category, fee, picture=None, user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.aprox_price = aprox_price
        self.category = category
        self.fee = fee
        self.picture = picture
        self.user_id = user_id

    def __str__(self):
        return f"[Service] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        picture_base64 = self.picture
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'aprox_price': self.aprox_price,
            'category': self.category,
            'fee': self.fee,
            'picture': picture_base64,
            'user_id': self.user_id,
            'appointments': [appointment.to_dict() for appointment in self.appointments],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def set_image(self, image_path):
        """Converts an image file to base64 and saves it in the picture attribute."""
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                self.picture = base64.b64encode(image_file.read()).decode('utf-8')  # Save to picture
        else:
            print("The image path is not valid.")
            self.picture = None

    @staticmethod
    def convert_image(image_path):
        """Converts an image file to a base64 string."""
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return encoded_string
        else:
            print("La ruta de la imagen no es válida.")
            return None
