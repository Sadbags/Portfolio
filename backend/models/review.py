from models.basemodel import BaseModel
from database import db

class Review(BaseModel):
    service_id = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.String(128), nullable=False)
    comment = db.Column(db.String(1024), nullable=True)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, service_id, user_id, comment, rating, **kwargs):
        super().__init__(**kwargs)
        self.service_id = service_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating


    def __str__(self):
        return f"[Review] ({self.id}) {self.to_dict()}"


    def to_dict(self):
        return {
			'id': self.id,
			'service_id': self.service_id,
			'user_id': self.user_id,
			'comment': self.comment,
			'rating': self.rating,
			'created_at': self.created_at.isoformat(),
			'updated_at': self.updated_at.isoformat()
		}
