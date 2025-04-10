import os
from flask_wtf import CSRFProtect
from flask import Flask
from flask_migrate import Migrate


csrf = CSRFProtect()


def create_app():
    from package.models import db

    app = Flask(__name__,instance_relative_config=1)
    app.config.from_pyfile('config.py')

    csrf.init_app(app)
    db.init_app(app)
    migrate = Migrate(app,db)

    return app

app = create_app()


from package import routes,form_routes,collection_routes,admin_routes
from package import forms