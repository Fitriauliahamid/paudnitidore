from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_ckeditor import CKEditor



app=Flask('__name__', template_folder='sim/templates', static_folder='sim/static')
app.config['SECRET_KEY']="timpaudni"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///paudni.db'
app.config['CKEDITOR_HEIGHT'] = 200
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager= LoginManager (app)
ckeditor = CKEditor (app)



#registasi blueprints

from sim.user.routes import guser
app.register_blueprint(guser)


from sim.admin.routes import gadmin
app.register_blueprint(gadmin)