from app import db

class Bitcoin(db.Model):
        __tablename__ = "data_bitcoin"
        date = db.Column(db.Date, primary_key=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        vol = db.Column(db.String(200))
        change = db.Column(db.String(200))

class EUR_USD(db.Model):
        __tablename__ = "data_EUR_USD"
        date = db.Column(db.Date, primary_key=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        change = db.Column(db.String(200))

class Gold(db.Model):
        __tablename__ = "data_gold"
        date = db.Column(db.Date, primary_key=True)
        price = db.Column(db.String(200))
        open = db.Column(db.String(200))
        high = db.Column(db.String(200))
        low = db.Column(db.String(200))
        change = db.Column(db.String(200))

class Nasdaq(db.Model):
    __tablename__ = "data_nasdaq"
    date = db.Column(db.Date, primary_key=True)
    price = db.Column(db.String(200))
    open = db.Column(db.String(200))
    high = db.Column(db.String(200))
    low = db.Column(db.String(200))
    vol = db.Column(db.String(200))
    change = db.Column(db.String(200))

class SP_Futures(db.Model):
   __tablename__ = "data_SP_futures"
   date = db.Column(db.Date, primary_key=True)
   price = db.Column(db.String(200))
   open = db.Column(db.String(200))
   high = db.Column(db.String(200))
   low = db.Column(db.String(200))
   vol = db.Column(db.String(200))
   change = db.Column(db.String(200)) 

class SP_VIX_Futures(db.Model):
   __tablename__ = "data_SP_VIX_futures"
   date = db.Column(db.Date, primary_key=True)
   price = db.Column(db.String(200))
   open = db.Column(db.String(200))
   high = db.Column(db.String(200))
   low = db.Column(db.String(200))
   vol = db.Column(db.String(200))
   change = db.Column(db.String(200)) 

class TSLA(db.Model):
   __tablename__ = "data_TSLA"
   date = db.Column(db.Date, primary_key=True)
   price = db.Column(db.String(200))
   open = db.Column(db.String(200))
   high = db.Column(db.String(200))
   low = db.Column(db.String(200))
   vol = db.Column(db.String(200))
   change = db.Column(db.String(200)) 