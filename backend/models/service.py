from database import db
from models.basemodel import BaseModel
import uuid

class Service(BaseModel):
    __tablename__ ='services'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    aprox_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(128), nullable=False)
    fee = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(1028), nullable=True)


    def __init__(self, name, description, aprox_price, category, fee, img_url=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.aprox_price = aprox_price
        self.category = category
        self.fee = fee
        self.img_url = img_url

    def __str__(self):
        return f"[Service] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'aprox_price': self.aprox_price,
            'category': self.category,
            'fee': self.fee,
            'img_url': self.img_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
