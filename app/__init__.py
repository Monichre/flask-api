# app/__init__.py
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

#initialize sql-alchemy
    # -- this is a ORM around the SQL database
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Bucketlist

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    # ---------------------------
    # Routes
    # ---------------------------

    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        # POST
        if request.method == 'POST':
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                reponse.status_code = 201
        else:
            # GET
            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):

        # Retrieve a bucket list using its ID
        bucketlist = Bucketlist.query.filter_by(id = id).first()

        if not bucketlist:
            # This means there is no bucketlist stored -- Throw and HTTPException error with a 404 message
            abort(404)
        if request.method == 'DELETE':
            bucketlist.delete()
            return {
            "message": "Bucketlist {} deleted successfully".format(bucketlist.id)
            }, 200

        elif request.method == "PUT":
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified

            })
            response.status_code = 200
            return response
        else:
            # Get
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response

    # Import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
