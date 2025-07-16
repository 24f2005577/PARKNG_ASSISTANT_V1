from spot import app, db
from spot.models import User, Admin, BookingHistory,ParkingLot, ParkingSpot
from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from datetime import datetime

def create_parking_lot(name,location,capacity,price_per_hour):
  if current_user.user_name != 'ADMIN':
    flash('You do not have permission to create a parking lot.', 'danger')
    return redirect(url_for('user_dashboard'))
  if ParkingLot.query.filter_by(parking_lot_name=name).first():
    flash("parking lot already exists", "danger")
  else:
    new_parking_lot = ParkingLot(
      parking_lot_name=name,
      parking_lot_location=location,
      parking_lot_capacity=capacity,
      price_per_hour=price_per_hour
    )
    db.session.add(new_parking_lot)
    db.session.commit()
    for spot_number in range (1,capacity+1):
      new_spot=ParkingSpot(
        parking_lot_id=new_parking_lot.parking_lot_id
      )
      db.session.add(new_spot)
    db.session.commit()
    flash(f'Parking lot {name} created successfully!', 'success') 
  return redirect(url_for('admin_dashboard'))

def release_booking(booking_id):
    booking = BookingHistory.query.filter_by(booking_id=booking_id).first()
    if booking:
        end_time = datetime.now()
        lot_id = booking.parking_lot_id
        price_per_hour = ParkingLot.query.filter_by(parking_lot_id=lot_id).first().price_per_hour
        price = (end_time - booking.start_time).total_seconds() / 3600 * price_per_hour
        booking.end_time = end_time
        booking.amount = price
        booking.status = False
        booking.parking_spot.is_available = True
        db.session.commit()
        flash(f'Booking {booking_id} released successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    else:
        flash('Booking not found', 'danger')
        return redirect(url_for('user_dashboard'))

def get_spot_id(lot_id):
   spot=ParkingSpot.query.filter_by(parking_lot_id=lot_id , is_available=True).first()
   if spot:
      return spot.parking_spot_id
   else:
      flash('No available parking spots in this lot', 'danger')
      return None
