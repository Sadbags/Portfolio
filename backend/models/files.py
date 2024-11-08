from backend.models.basemodel import BaseModel
from backend.database import db


class Files(BaseModel):
    __tablename__ = 'files'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    docs_id = db.Column(db.String(36), db.ForeignKey('docs.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(50), nullable=False)

    document = db.relationship('Docs', back_populates='files', foreign_keys='Files.docs_id')
    user = db.relationship('User', back_populates='files')

    def __init__(self, user_id, filename, file_url, file_size, file_type, docs_id, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.filename = filename
        self.file_url = file_url
        self.file_size = file_size
        self.file_type = file_type
        self.docs_id = docs_id

    def __str__(self):
        return f"[Files] ({self.id}) {self.to_dict()}"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_url': self.file_url,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'docs_id': self.docs_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
            }
