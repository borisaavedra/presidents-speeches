from application import db

class Speeches(db.Model):
    __tablename__ = "speeches"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    date_s = db.Column(db.DateTime)
    speech = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(200), nullable=True)
    len_s = db.Column(db.Integer, nullable=True)
    time_s = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<President %r>" % self.name