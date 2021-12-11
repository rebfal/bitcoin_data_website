from app import db

class Bitcoin(db.Model):
        __tablename__ = "data_bitcoin"
        date = db.Column(db.Date, primary_key=True, unique=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        vol = db.Column(db.String(200))
        change = db.Column(db.String(200))

class EUR_USD(db.Model):
        __tablename__ = "data_EUR_USD"
        date = db.Column(db.Date, primary_key=True, unique=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        change = db.Column(db.String(200))