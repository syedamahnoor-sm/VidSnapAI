from database import db
from datetime import datetime

class Reel(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    description = db.Column(db.Text)

    status = db.Column(db.String(50), default="pending")

    audio_path = db.Column(db.String(500))

    video_path = db.Column(db.String(500))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)