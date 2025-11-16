from spotx import db, app, login_manager,cipher
from spotx.model import User, Lot, Spot, BookingHistory
from spotx.function import create_user, create_lot, add_spot_fun,book_spot, end_booking,DeleteLot,delete_spot_fun,search,commit_booking,dummy_end_booking,update_user
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from spotx.forms import loginForm, register_user,submit_Form, createLotForm, UpdateUserForm,UserSearchForm,bookSpotForm, end_bookingForm,release_Form,AddSpotForm,UpdateLotForm, searchForm

@app.route('/')
def base():
    return render_template('guest_index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(attempted_password=form.password.data):
            login_user(user)
            if user.id == 1:
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    
    for err in form.errors:
        for er in form.errors[err]:
            flash(f'Error: {er}', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=register_user()
    if form.validate_on_submit():
        user = create_user(username=form.username.data, email=form.email.data, password=form.password.data, phone_number=form.phone_number.data,address=form.address.data, pincode=form.pincode.data)
        if user:
            login_user(user)
            flash('Registration successful! You are now logged in.', 'success')
            return redirect(url_for('dashboard'))
    
    for err in form.errors:
        for er in form.errors[err]:
            flash(f'{er}', 'danger')
        
    return render_template('register.html', form=form)



@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    
    lots = Lot.query.all()
    spots=Spot.query.all()
    return render_template('admin_dashboard.html',  lots=lots, spots=spots)

@app.route('/create_lot', methods=['GET', 'POST'])
@login_required
def create_lot_route():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = createLotForm()
    if form.validate_on_submit():
        lot = create_lot(name=form.name.data, description=form.description.data, 
                          location=form.location.data, price_per_hour=form.price_per_hour.data, 
                          no_of_spots=form.no_of_spots.data, address=form.address.data, pincode=form.pincode.data)
        if lot:
            return redirect(url_for('admin_dashboard'))
    
    for err in form.errors:
        for er in form.errors[err]:
            flash(f'Error: {er}', 'danger')
    
    return render_template('create_lot.html', form=form)

@app.route('/view_lot', methods=['GET', 'POST'])
@login_required
def view_lot():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    
    encrypt = request.args.get('encrypt')
   
    lot_id = cipher.decrypt(encrypt).decode('utf-8')
    lot = Lot.query.get(lot_id)
   

    
    form = UpdateLotForm()
    spoter=AddSpotForm()

    
    if form.validate_on_submit():
        lot.name = form.name.data
        lot.location = form.location.data
        lot.price_per_hour = form.price_per_hour.data
        lot.description=form.des.data
        lot.address=form.address.data
        lot.pincode=form.pincode.data
        db.session.commit()
        flash('Parking lot updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    elif request.method == 'GET':
        form.name.data = lot.name
        form.description.data = lot.description
        form.location.data = lot.location
        form.des.data=lot.description
        form.address.data=lot.address
        form.pincode.data=lot.pincode
        form.price_per_hour.data = lot.price_per_hour
        form.no_of_spots.data = lot.no_of_spots

    return render_template('view_lot.html', lot=lot, form=form, spoter=spoter)

@app.route('/view_spot')
@login_required
def view_spot():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    
    form=submit_Form()
    encrypt = request.args.get('encrypt')
    spot_id = cipher.decrypt(encrypt).decode('utf-8')
    spot = Spot.query.get(spot_id)
    if not spot:
        flash('Spot not found.', 'danger')
        return redirect(url_for('admin_dashboard'))


    return render_template('view_spot.html', spot=spot, form=form)

@app.route('/delete_spot', methods=['POST','GET'])
@login_required
def delete_spot():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))

    encrypt = request.args.get('encrypt')
    spot_id = cipher.decrypt(encrypt).decode('utf-8')
    delete_spot_fun(spot_id)
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/search_admin', methods=['GET', 'POST'])
@login_required
def search_admin():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = searchForm()
    results = []
    spots= Spot.query.all()
    
    if form.validate_on_submit():
        results = search(category=form.category.data, search_term=form.search.data)
        if form.category.data=='username' or form.category.data=='email' or form.category.data=='user_id':
            return render_template('user_list.html',form=form,users=results)
        else :
            return render_template('search_lot.html', form=form, result=results, spots=spots)



    return render_template('search_admin.html', form=form, results=results, spots=spots)

@app.route('/add_spot', methods=['POST'])
@login_required
def add_spot():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    
    
    encrypt = request.args.get('encrypt')
    lot_id = int(cipher.decrypt(encrypt).decode('utf-8'))
    form=AddSpotForm()
    if form.validate_on_submit():
        num_spots = form.num_spots.data
    
    add_spot_fun(lot_id, num_spots)
    return redirect(url_for('admin_dashboard'))

@app.route('/user_list')
@login_required
def user_list():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))

    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/deletelot', methods=['GET', 'POST'])
@login_required
def delete_lot():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
           
    encrypt = request.args.get('encrypt')
    lot_id = int(cipher.decrypt(encrypt).decode('utf-8'))
    DeleteLot(lot_id)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_summary')
@login_required
def admin_summary():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    bookings = BookingHistory.query.all()
    lots= Lot.query.all()
    lot_labels = [lot.name for lot in lots]
    bookings_per_lot = [sum(int(1) for b in bookings if b.lot_id == lot.id) for lot in lots]
    revenue_per_lot = [sum(b.total_amount for b in bookings if b.lot_id == lot.id) for lot in lots]
    total_spots = Spot.query.count()
    total_occupied = Spot.query.filter_by(is_occupied=True).count()
    pieoccupy=[total_spots-total_occupied, total_occupied]
    user_labels = list(set(book.parker.username for book in bookings if book.parker))  # Changed to user_labels
    user_spends = [sum(b.total_amount or 0 for b in bookings if b.parker and b.parker.username == user) for user in user_labels]

    return render_template(
        'admin_summary.html',
        lot_labels=lot_labels,
        bookings_per_lot=bookings_per_lot,
        revenue_per_lot=revenue_per_lot,
        pieoccupy=pieoccupy,
        user_label=user_labels,
        user_spends=user_spends)

@app.route('/spot_details', methods=['POST'])
@login_required
def spot_details():
    if current_user.id != 1:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('dashboard'))
    form=submit_Form()
    encrypt = request.args.get('encrypt')
    spot_id = int(cipher.decrypt(encrypt).decode('utf-8'))
    history = BookingHistory.query.filter_by(spot_id=spot_id, end_time=None).first()
    if not history:
        flash('Spot not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    return render_template('spot_details.html', history=history, form=form)

#client-side code to run the app




@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    lots=Lot.query.all()
    bookd=BookingHistory.query.filter_by(parker_id=current_user.id).order_by(BookingHistory.start_time.desc()).all()
    results = []
    results=lots
    form=UserSearchForm()
    form1=release_Form()
    if form.validate_on_submit():
        results = search(category=form.category.data, search_term=form.search.data)
        return render_template('dashboard.html', bookd=bookd, results=results, form=form, form1=form1)
    return render_template('dashboard.html', bookd=bookd, results=lots, form=form, form1=form1)

@app.route('/book_spot', methods=['GET', 'POST'])
@login_required
def book_spot_route():
    form = bookSpotForm()
    encrypt= request.args.get('encrypt')
    lot_id = int(cipher.decrypt(encrypt).decode('utf-8'))
    result= book_spot(current_user.id,lot_id)
    if result is None:
        flash('No available spots in this parking lot.', 'warning')
        return redirect(url_for('dashboard'))
    booking, num = result
    form.start_time.data =booking.start_time
    form.lot_id.data = booking.lot_id
    form.spot_id.data = booking.spot_id
    form.spot_name.data = num

    for err in form.errors:
        for er in form.errors[err]:
            flash(f'Error: {er}', 'danger')
    
    return render_template('book_spot.html', form=form)

@app.route('/commit_book', methods=['POST'])
@login_required
def commit_book():
    form = bookSpotForm()
    if form.validate_on_submit():
        spot_id = form.spot_id.data
        lot_id = form.lot_id.data
        vehicle_number = form.vehicle_number.data
        start_time = form.start_time.data
        flash('Booking successful!', 'success')


    final=commit_booking(current_user.id, lot_id, spot_id, start_time, vehicle_number)
    for err in form.errors:
        for er in form.errors[err]:
            flash(f'Error: {er}', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/end_booking', methods=['POST'])
@login_required
def end_booking_route():
    form=end_bookingForm()
    form1=release_Form()
    encrypt = request.args.get('encrypt')
    booking_id = int(cipher.decrypt(encrypt).decode('utf-8'))
    book=dummy_end_booking(booking_id)
    return render_template('release.html', book=book,form=form,form1=form1)

@app.route('/ended_booking', methods=['POST'])
@login_required
def ended_booking():
    encrypt = request.args.get('encrypt')
    booking_id = int(cipher.decrypt(encrypt).decode('utf-8'))
    end_booking(booking_id)
   
    return redirect(url_for('dashboard'))

@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = UpdateUserForm()
    if form.validate_on_submit():
     
        if form.password.data and form.password.data != form.confirm_password.data:
            flash('Passwords do not match.', 'danger')
        password_to_update= form.password.data if form.password.data else None
        address_to_update=form.address.data if form.address.data else None
        pincode_to_update=form.pincode.data if form.pincode.data else None
        user = update_user(current_user.id, form.username.data, form.email.data,form.phone_number.data, address_to_update,pincode_to_update, password_to_update)
        return redirect(url_for('dashboard'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.address.data = current_user.address
        form.pincode.data = current_user.pincode
    
    return render_template('update_user.html', form=form)

@app.route('/summary')
@login_required
def summary():
    user_bookings = BookingHistory.query.filter_by(parker_id=current_user.id).order_by(BookingHistory.start_time).all()
    labels=[]
    lots = Lot.query.all()
    for lot in lots:
        labels.append(lot.name)
    bookings_per_lot = [BookingHistory.query.filter_by(lot_id=lot.id).count() for lot in Lot.query.all()]
    price_per_lot = [sum(b.total_amount for b in BookingHistory.query.filter_by(lot_id=lot.id).all()) for lot in Lot.query.all()]

    return render_template('user_summary.html', labels=labels, bookings_per_lot=bookings_per_lot, price_per_lot=price_per_lot)
@app.route('/bill')
@login_required
def bill():
    encrypt = request.args.get('encrypt')
    booking_id = int(cipher.decrypt(encrypt).decode('utf-8'))
    booking = BookingHistory.query.get(booking_id)
    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('bill.html', book=booking)


