from jump import db
from sqlalchemy import func

class GRedirect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(255))
    url = db.Column(db.String(2047))
    short_name = db.Column(db.String(31), unique=True)
    created_date = db.Column(db.DateTime, default=func.current_timestamp)
    modified_date = db.Column(db.DateTime, onupdate=func.current_timestamp)

    def __init__(self, owner, url, short_name):
        self.owner = owner
        self.url = url
        self.short_name = short_name
