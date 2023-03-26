import os
from flask_admin import Admin
from models import db, User, Character, Location, Episode
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap4')

    class MyModel(ModelView):
        column_display_pk = True
        column_display_fk = True

    admin.add_view(MyModel(User, db.session))
    admin.add_view(MyModel(Character, db.session))
    admin.add_view(MyModel(Location, db.session))
    admin.add_view(MyModel(Episode, db.session))
