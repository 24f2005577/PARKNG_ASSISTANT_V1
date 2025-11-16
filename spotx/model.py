from spotx import db, Bcrypt, login_manager, cipher
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    parking_history = db.relationship('BookingHistory', backref='parker', lazy=True)
    encrypted_id = db.Column(db.String(150), nullable=True, unique=True)

    @property 
    def password(self):
        pass
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = Bcrypt.generate_password_hash(plain_text_password).decode('UTF-8')
    
    def check_password(self, attempted_password):
        return Bcrypt.check_password_hash(self.password_hash, attempted_password)

    def save_and_encrypt(self):
        db.session.add(self)
        db.session.commit()
        if not self.encrypted_id:
            self.encrypted_id = cipher.encrypt(str(self.id))
            db.session.commit()
            return self


class Lot(db.Model):
    __tablename__ = 'lots'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(150), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False, default=0.0)
    no_of_spots = db.Column(db.Integer, nullable=False, default=0)
    address=db.Column(db.String(150),nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    spots = db.relationship('Spot', backref='lot', lazy=True)
    encrypted_id= db.Column(db.String(150), nullable=True, unique=True)


    def save_and_encrypt(self):
        db.session.add(self)
        db.session.commit()  # Get the ID first
        if not self.encrypted_id:
            self.encrypted_id = cipher.encrypt(str(self.id))
            db.session.commit()  
        return self


class Spot(db.Model):
    __tablename__ = 'spots'
    
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, nullable=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    parking_history = db.relationship('BookingHistory', backref='spot', lazy=True)
    encrypted_id=db.Column(db.String(150), nullable=True, unique=True)

    def save_and_encrypt(self):
        db.session.add(self)
        db.session.commit()  # Get the ID first
        if not self.encrypted_id:
            self.encrypted_id = cipher.encrypt(str(self.id))
            db.session.commit()  
        return self


class BookingHistory(db.Model):
    __tablename__ = 'booking_history'
    
    id = db.Column(db.Integer, primary_key=True)
    parker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('spots.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    total_amount = db.Column(db.Float, nullable=False, default=10)
    encrypted_id = db.Column(db.String(150), nullable=True, unique=True)

    def save_and_encrypt(self):
        db.session.add(self)
        db.session.commit()
        if not self.encrypted_id:
            self.encrypted_id = cipher.encrypt(str(self.id))
            db.session.commit()
        return self
