from backend.database import db
from backend.models.basemodel import BaseModel
import uuid
import base64

class Service(BaseModel):
    __tablename__ ='services'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    aprox_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(128), nullable=False)
    fee = db.Column(db.Float, nullable=False)
    img_data = db.Column(db.LargeBinary, nullable=True)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='services')  # esto es lo nuevo
    reviews = db.relationship('Review', back_populates='service')  # esto es lo nuevo


    def __init__(self, name, description, aprox_price, category, fee, img_data=None, user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.aprox_price = aprox_price
        self.category = category
        self.fee = fee
        self.img_data = img_data
        self.user_id = user_id

    def __str__(self):
        return f"[Service] ({self.id}) {self.to_dict()}"



    def to_dict(self):
        img_base64 = base64.b64encode(self.img_data).decode('utf-8') if self.img_data else None
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'aprox_price': self.aprox_price,
            'category': self.category,
            'fee': self.fee,
            'img_data': img_base64,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
