from flask_restx import Namespace, Resource, fields
from models.user import User
from models.roles import Roles
from flask_jwt_extended import jwt_required
from extensions import db


def create_crud_user_namespace():
    api = Namespace("User_Crud", description="User CRUD operations")

    user_model = api.model(
        "User",
        {
            "id": fields.Integer(
                readOnly=True, description="The unique identifier of a user"
            ),
            "username": fields.String(required=True, description="User login name"),
            "password": fields.String(required=True, description="User password"),
            "role_id": fields.Integer(
                description="Role ID of the user"
            ), 
        },
    )

    @api.route("/")
    class UserList(Resource):
        @jwt_required()
        def get(self):
            """Retrieve all user"""
            users = User.query.all()
            return api.marshal(users, user_model), 200

        @api.expect(user_model)
        def post(self):
            """'Create a new user"""
            data = api.payload
            user = User(username=data["username"])
            user.set_password(data["password"])
            user.role_id = data.get("role_id")  # Expecting role_id in the payload
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully"}, 201

    @api.route("/<int:id>")
    @api.response(404, "User not found")
    @api.param("id", "User not found")
    class User_Update_Delete(Resource):
        @jwt_required()
        def get(self, id):
            """Retrieve a user by id"""
            user = User.query.get_or_404(id)
            return api.marshal(user, user_model), 200

        @api.expect(user_model)
        def put(self, id):
            """Update a user given its identifier"""
            user = User.query.get_or_404(id)
            data = api.payload
            user.username = data["username"]
            user.set_password(data["password"])
            db.session.commit()
            return {"message": "User updated successfully"}, 200

        @jwt_required()
        def delete(self, id):
            """Delete a user given its identifier"""
            user = User.query.get_or_404(id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 204
        

    @api.route('/<int:user_id>/role/<int:role_id>')
    class UserRoleUpdate(Resource):
        @jwt_required()
        def put(self, user_id, role_id):
            user = User.query.get_or_404(user_id)
            role = Roles.query.get(role_id)
            if not role:
                return {"message": "Role not found"}, 404

            user.role_id = role.role_id
            db.session.commit()
            return {"message": "User role updated successfully"}, 200


    return api
