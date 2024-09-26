from backend.models.basemodel import BaseModel
from backend.database import db


class Docs(BaseModel):
    __tablename__ = 'docs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(128), nullable=False)
    file_id = db.Column(db.String(128), db.ForeignKey('files.id'), nullable=False)
    doc_type = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), nullable=False)

    user = db.relationship('User', back_populates="docs")
    files = db.relationship('Files', back_populates='document', foreign_keys='Files.docs_id')

    def __init__(self, user_id, title, content, file_id, doc_type, status, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.title = title
        self.content = content
        self.file_id = file_id
        self.doc_type = doc_type
        self.status = status


    def __str__(self):
        return f"[Docs] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
			'id': self.id,
			'user_id': self.user_id,
			'title': self.title,
			'content': self.content,
			'file_id': self.file_id,
			'doc_type': self.doc_type,
			'status': self.status,
			'created_at': self.created_at.isoformat(),
			'updated_at': self.updated_at.isoformat()
		}
