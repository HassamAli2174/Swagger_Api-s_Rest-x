from flask_restx import Namespace, Resource, fields
from flask import request
from sqlalchemy.exc import IntegrityError
from models.user import User
from extensions import db
# from services.auth_service import encode_auth_token, decode_auth_token
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)


def create_auth_namespace():
    api = Namespace("Auth", description="Authentication related operations", security='Bearer Auth')

    user_model = api.model(
        "User",
        {
            "username": fields.String(required=True, description="The username"),
            "password": fields.String(required=True, description="The password"),
        },
    )

    ####################################################################################################
    # def token_required(f):
    #     @wraps(f)
    #     def decorated(*args, **kwargs):
    #         auth_header = request.headers.get("Authorization")
    #         if not auth_header:
    #             return {"error": "Token is missing!"}, 401
    #         try:
    #             auth_token = auth_header.split(" ")[1]
    #             user_id = decode_auth_token(auth_token)
    #             if isinstance(user_id, str):
    #                 return {"error": user_id}, 401
    #         except Exception as e:
    #             return {"error": "Token is invalid!"}, 401

    #         return f(user_id, *args, **kwargs)

    #     return decorated

    ####################################################################################################
    @api.route("/register")
    class Register(Resource):
        @api.expect(user_model)
        @api.doc("register_user")
        def post(self):
            print("Received registration request")
            data = request.get_json()
            print(f"Data received: {data}")
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                print("Username or password missing")
                return {"error": "Username and password required"}, 400

            new_user = User(username=username)
            new_user.set_password(password)

            try:
                db.session.add(new_user)
                db.session.commit()
                print("User added to database")
                return {"message": "User registered successfully"}, 201
            except IntegrityError:
                db.session.rollback()
                print(f"IntegrityError: {e}")
                return {"error": "Username already exists"}, 409
            except Exception as e:
                db.session.rollback()
                print(f"Unexpected error: {e}")
                return {"error": "An error occurred during registration"}, 500

    @api.route("/login")
    class Login(Resource):
        @api.expect(user_model)
        @api.doc("login_user")
        # @jwt_required() 
        def post(self):
            # user = get_jwt_identity()
            try:
                print("Received login request")
                data = request.get_json()
                print(f"Data received: {data}")

                username = data.get("username")
                password = data.get("password")

                print(f"Username: {username}, Password: {password}")

                # Check if the username exists in the database
                user = User.query.filter_by(username=username).first()
                if user:
                    print(f"User found in database: {user.username}")
                else:
                    print(f"No user found with username: {username}")

                # Verify the password
                if user and user.check_pwd_hash(password):
                    print(f"Password check passed for user: {user.username}")

                    access_token = create_access_token(identity=user.id)
                    refresh_token = create_refresh_token(identity=user.id)

                    response_data = {
                        "message": "Login successful",
                        "refresh_token": refresh_token,
                        "access_token": access_token,
                        "username": user.username,
                    }
                    print(f"Returning response: {response_data}")
                    return response_data, 200  
                else:
                    print("Invalid credentials provided")
                    return {"error": "Invalid credentials"}, 401

            except Exception as e:
                print(f"Unexpected error: {e}")
                return {"error": "An error occurred during login"}, 500

    @api.route("/protected")
    class ProtectedResource(Resource):
        @api.doc(security='Bearer Auth')
        @jwt_required()  # Protect this route with JWT
        def get(self):
            current_user_id = get_jwt_identity()
            return {
                "message": f"Hello, user {current_user_id}. You have access to this resource."
            }, 200

    # @api.route("/refresh")
    # class RefreshToken(Resource):
    #     @jwt_required(refresh=True)
    #     def refresh():
    #         user_id = get_jwt_identity()
    #         access_token = create_access_token(identity=user_id)
    #         return {"access_token": access_token}, 200

    return api
