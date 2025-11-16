from spotx import db,app
from spotx.routes import *
from spotx.model import User
from spotx.function import create_user

with app.app_context():
    db.create_all()
    if not User.query.first():
        user=User(id=1,username='ADMIN',email='ADMIN@ADMIN.ADMIN',phone_number='0000000001',address='ADMIN ADDRESS',pincode='000000')
        user.password='123456'
        user=user.save_and_encrypt()

if __name__ == '__main__':
    app.run(debug=True)