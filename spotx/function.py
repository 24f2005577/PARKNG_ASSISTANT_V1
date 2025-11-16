from  spotx import app , db 
from spotx.model import User, Lot, Spot, BookingHistory
from flask_login import  current_user
from flask import flash 
from datetime import datetime

def create_user(username, email, password, phone_number,address=None, pincode=None):
    if User.query.filter_by(username=username).first():
        flash('Username already exists. Please choose a different one.', 'danger')
        return None
    if User.query.filter_by(email=email).first():
        flash('Email already registered. Please use a different email.', 'danger')
        return None
    if User.query.filter_by(phone_number=phone_number).first():
        flash('Phone number already registered. Please use a different phone number.', 'danger')
        return None
    new_user = User(username=username, email=email)
    new_user.password = password
    if address:
        new_user.address = address
    if pincode:
        new_user.pincode = pincode
    new_user.phone_number = phone_number
    new_user = new_user.save_and_encrypt()
    return new_user

def create_lot(name, description, location, price_per_hour, no_of_spots, address, pincode):
    new_lot = Lot(name=name, description=description, location=location, 
                  price_per_hour=price_per_hour, no_of_spots=no_of_spots, address=address, pincode=pincode)
    new_lot = new_lot.save_and_encrypt()  
    if not new_lot:
        flash('Error creating parking lot. Please try again.', 'danger')
        return None
    k=int(no_of_spots)
    for i in range(1,k+1):
        
        new_spot = Spot(lot_id=new_lot.id, spot_id=i)
        new_spot = new_spot.save_and_encrypt()
    flash('Parking lot created successfully!', 'success')
    return new_lot

def book_spot(user_id, lot_id):
    lot = Lot.query.get(lot_id)
    if not lot:
        flash('Parking lot not found.', 'danger')
        return None
    
    available_spot = Spot.query.filter_by(lot_id=lot_id, is_occupied=False).first()
    if not available_spot:
        return None
    start_time = datetime.now()
    new_booking = BookingHistory(parker_id=user_id, lot_id=lot_id, spot_id=available_spot.id, start_time=start_time)

    return new_booking, available_spot.spot_id

def commit_booking(user_id, lot_id, spot_id, start_time, vehicle_number):
    new_booking = BookingHistory(parker_id=user_id, lot_id=lot_id, spot_id=spot_id,
                                 vehicle_number=vehicle_number, start_time=start_time)
    
    new_booking = new_booking.save_and_encrypt()

    new_booking.spot.is_occupied = True
    db.session.commit()
    
    return new_booking
    

def add_spot_fun(lot_id,num_spots):
    lot = Lot.query.get(lot_id)
    highest_spot = Spot.query.filter_by(lot_id=lot_id).order_by(Spot.spot_id.desc()).first()
    next_spot_id = highest_spot.spot_id+1
    
    num_spots = int(num_spots)
    for i in range(num_spots):
        new_spot = Spot(lot_id=lot.id, spot_id=next_spot_id + i)
        new_spot = new_spot.save_and_encrypt()
    flash(f'{num_spots} spots added successfully! to {lot.name}', 'success')

    lot.no_of_spots += num_spots
    db.session.commit()
    
def dummy_end_booking(booking_id):
    booking = BookingHistory.query.get(booking_id)
    if not booking:
        flash('Booking not found.', 'danger')
        return None
    
    if booking.end_time:
        return None
    
    booking.end_time = datetime.now()
    booking.spot.is_occupied = False
    total_duration = (booking.end_time - booking.start_time).total_seconds() / 3600  # in hours
    if total_duration < 1:
        total_duration = 1
    booking.total_amount = round( total_duration * booking.spot.lot.price_per_hour ,2)

    return booking
  


def end_booking(booking_id):
    booking = BookingHistory.query.get(booking_id)
    if not booking:
        flash('Booking not found.', 'danger')
        return None
    
    if booking.end_time:
        flash('Booking already ended.', 'info')
        return None
    
    booking.end_time = datetime.now()
    booking.spot.is_occupied = False
    total_duration = (booking.end_time - booking.start_time).total_seconds() / 3600  # in hours
    if total_duration < 1:
        total_duration = 1
    booking.total_amount = round( total_duration * booking.spot.lot.price_per_hour ,2)


    
    db.session.commit()
    
    flash('Booking ended successfully!', 'success')
    return booking

def update_user(user_id, username, email, phone_number,address=None, pincode=None, password=None):
   
    user = User.query.get(user_id)
    
    case1= User.query.filter(User.username == username, User.id != user_id).first()
    case2= User.query.filter(User.email == email, User.id != user_id).first()
    case3= User.query.filter(User.phone_number == phone_number, User.id != user_id).first()
    if case1:
        flash('Username already exists. Please choose a different one.', 'danger')
        return None
    if case2:
        flash('Email already registered. Please use a different email.', 'danger')
        return None
    if case3:
        flash('Phone number already registered. Please use a different phone number.', 'danger')
        return None
    else: 
        user.username = username
        user.email = email
        user.phone_number = phone_number
        if password:
            user.password = password
        if address:
            user.address = address
        if pincode:
            user.pincode = pincode
        
        user = user.save_and_encrypt()
        flash('User updated successfully!', 'success')
        db.session.commit()  
 
    return user

    
    


def delete_spot_fun(spot_id):
    spot = Spot.query.get(spot_id)
    if not spot:
        flash('Spot not found.', 'danger')
        return None
    
    if spot.is_occupied:
        flash('Cannot delete an occupied spot.', 'warning')
        return None
    

    spot.lot.no_of_spots -= 1
    db.session.delete(spot)
    db.session.commit()
    flash('Spot deleted successfully!', 'success')
    return spot

def search(category, search_term):
    if category == 'username':
        return User.query.filter(User.username.ilike(f'%{search_term}%')).all()
    elif category == 'email':
        return User.query.filter(User.email.ilike(f'%{search_term}%')).all()
    elif category == 'user_id':
        search_term= int(search_term)
        return User.query.filter(User.id == search_term).all()
    elif category == 'lot_id':
        search_term = int(search_term)
        return Lot.query.filter(Lot.id == search_term).all()
    elif category == 'lot_location':
        return Lot.query.filter(Lot.location.ilike(f'%{search_term}%')).all()
    elif category == 'lot_name':
        return Lot.query.filter(Lot.name.ilike(f'%{search_term}%')).all()
    elif category == 'pincode':
        return Lot.query.filter(Lot.pincode == int(search_term)).all()
    
    else:
        flash('Invalid search category.', 'danger')
        return []

def DeleteLot(lot_id):
    lot = Lot.query.get(lot_id)
    for spot in lot.spots:
        if spot.is_occupied:
            flash('Cannot delete a parking lot with occupied spots.', 'warning')
            return None
    for spot in lot.spots:
        db.session.delete(spot)
    db.session.commit()
    db.session.delete(lot)
    db.session.commit()
    flash('Parking lot deleted successfully!', 'success')

def UserSearch(category, search_term):
    if category == 'lot_id':
        search_term = int(search_term)
        return Lot.query.filter(Lot.id == search_term).all()
    elif category == 'lot_location':
        return Lot.query.filter(Lot.location.ilike(f'%{search_term}%')).all()
    elif category == 'lot_name':
        return Lot.query.filter(Lot.name.ilike(f'%{search_term}%')).all()
    elif category == 'pincode':
        return Lot.query.filter(Lot.pincode == int(search_term)).all()
    
    else:
        flash('Invalid search category.', 'danger')
        return []

