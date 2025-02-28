from flask import Flask



def BUILD():
    from .views import views, init_db

    app = Flask(__name__)

    init_db()
    app.register_blueprint(views)

    return app