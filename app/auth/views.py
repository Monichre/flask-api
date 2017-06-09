from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):

    # Handle the POST request for this view
    def post(self):

        # Query the database to see if a user exists
        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # Make a new User
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']

                # Instantiate new User Object
                user = User(email=email, password=password)
                user.save()

                response = {
                    'message': "You have registered successfully. Please log in."
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                # Return error string
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # A user exists -- dont register twice
            response = {
                'message': 'User already exists. Please log in'
            }
            return make_response(jsonify(message)), 202

# Define the rule for the registration url ---> /auth/register
registration_view = RegistrationView.as_view('register_view')

# Add the rule to the Blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])
