from spot import app,db
from flask import render_template,redirect,url_for
from spot.forms import LoginForm,RegisterForm
from spot.models import User,Admin
from flask import flash
from flask_login import login_user,login_required


@app.route('/')#index page
def guest_index():
  return render_template('guest_index.html')

@app.route('/login',methods=['POST','GET'])  #login page
def login():
  form=LoginForm()
  if form.validate_on_submit(): #validating the form
    usr_obj=User.query.filter_by(user_name=form.username.data).first()
    if not(usr_obj):
      flash('INVALID USERNAME',category='danger')
    elif usr_obj.check_password(attempted_password=form.password.data):
      login_user(usr_obj)
      flash(f'WELCOME {usr_obj.user_name}',category='success')
      return redirect(url_for("home")) #successful redirection to home page
    else:
      flash('INVALID PASSWORD','danger')
  return render_template('login_page.html',form=form)

@app.route('/register', methods=['POST', 'GET']) #sign up page
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(user_name=form.username.data).first():
            flash('USER NAME EXISTS', 'danger')
        elif User.query.filter_by(user_email=form.email.data).first():
            flash('EMAIL ALREADY EXISTS', 'danger')
        elif User.query.filter_by(mobile_no=form.phone.data).first():
            flash('MOBILE NO ALREADY EXISTS', 'danger')
        else:
            new_user = User(
                user_name=form.username.data,
                user_email=form.email.data,
                mobile_no=form.phone.data,
                password=form.password1.data  
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash(f'WELCOME {new_user.user_name}',category='success')
            return redirect(url_for("home")) #successful redirection to home page
    if form.errors:
             for err_list in form.errors.values():
               for err in err_list:
                 flash(err, 'danger')
    return render_template('registration.html', form=form)
   
@app.route('/home')
@login_required
def home():
  return render_template('home.html')
