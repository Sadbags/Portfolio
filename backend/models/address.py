from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import db
from backend.models.basemodel import BaseModel

#esta tabla esta terminada funciona con users api

class Address(BaseModel):
    __tablename__ = 'addresses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    address = db.Column(db.String(128), nullable=True)
    street = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates="addresses")

    def __init__(self, street, city, state, zip_code, phone, user_id, address, **kwargs):
        super().__init__(**kwargs)
        self.address = address
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.user_id = user_id

    def __str__(self):
        return f"[Address] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
