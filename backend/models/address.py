from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import db
from backend.models.basemodel import BaseModel

#esta tabla esta terminada funciona con users api

class Address(BaseModel):
    __tablename__ = 'addresses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    street = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    users = db.relationship('User', back_populates="addresses")

    def __init__(self, street, city, state, zip_code, user_id, **kwargs):
        super().__init__(**kwargs)
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.user_id = user_id

    def __str__(self):
        return f"[Address] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
