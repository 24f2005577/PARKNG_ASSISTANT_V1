from spot import db,bcrypt,login_manager
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    user_email = db.Column(db.String(70), nullable=False, unique=True)
    mobile_no = db.Column(db.String(15), nullable=False, unique=True)
    password_hash = db.Column(db.String(70), nullable=False)
    parking_history = db.relationship('BookingHistory', backref='parker', lazy=True)
     
    @property
    def id(self):
        return self.user_id
    @property 
    def password(self):
        pass
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('UTF-8')
    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

class Admin(db.Model,UserMixin):
    __tablename__ = 'admin'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    id= db.Column(db.Integer, primary_key=True)
    admin_user_name = db.Column(db.String(30), nullable=False, unique=True)
    password_hash = db.Column(db.String(70), nullable=False)

     
    @property 
    def password(self):
        pass
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('UTF-8')
    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)




class BookingHistory(db.Model):
    __tablename__ = 'booking_history'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.parking_lot_id'), nullable=False)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.parking_spot_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime,nullable=True)
    status=db.Column(db.Boolean, nullable=False, default=True)  # True for active booking, False for complete
    amount = db.Column(db.Float, nullable=False,default=0)

class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    parking_lot_id = db.Column(db.Integer, primary_key=True)
    parking_lot_name = db.Column(db.String(30), nullable=False, unique=True)
    parking_lot_location = db.Column(db.String(100), nullable=False)
    parking_lot_capacity = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False, default=10.0)  # <-- Add this line
    current_occupancy = db.Column(db.Integer, default=0)
    parking_lots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True)




class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    parking_spot_id = db.Column(db.Integer, primary_key=True)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.parking_lot_id'))
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    booking_history = db.relationship('BookingHistory', backref='parking_spot', lazy=True)