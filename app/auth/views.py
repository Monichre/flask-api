from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):

    # Handle the POST request for this view 'auth/register'
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
            return make_response(jsonify(response)), 202

class LoginView(MethodView):

    # Handle the POST request for this view 'auth/login'
    def post(self):

        # Get the user by their email
        try:
            user= User.query.filter_by(email=request.data['email']).first()

            # Authenticate the user using their password
            if user and user.password_is_valid(request.data['password']):
                # Generate the access token
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': "You logged in successfully",
                        "access_token": access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Return error
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


# Define the rule for the registration url ---> /auth/register
registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

# Add the rule to the Blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST'])
