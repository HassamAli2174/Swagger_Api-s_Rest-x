from flask_restx import Resource, fields, Namespace
from extensions import db
from models.roles import Roles


def create_roles_namespace():
    api = Namespace("roles", description="Roles operations")

    role_model = api.model(
        "Role",
        {
            "role_id": fields.Integer(description="Role ID"),
            "role_name": fields.String(required=True, description="Name of the Role"),
        },
    )
    
    @api.route('/')
    class RoleList(Resource):
        @api.doc('list_roles')
        @api.marshal_list_with(role_model)
        def get(self):
            """List all roles"""
            roles = Roles.query.all()
            return roles

        @api.doc('create_role')
        @api.expect(role_model)
        @api.marshal_with(role_model, code=201)
        def post(self):
            """Create a new role"""
            data = api.payload
            new_role = Roles(role_name=data['role_name'])
            db.session.add(new_role)
            db.session.commit()
            return new_role, 201

    @api.route('/<int:role_id>')
    @api.response(404, 'Role not found')
    @api.param('role_id', 'The Role identifier')
    class Role(Resource):
        @api.doc('get_role')
        @api.marshal_with(role_model)
        def get(self, role_id):
            """Fetch a role given its identifier"""
            role = Roles.query.get_or_404(role_id)
            return role

        @api.doc('update_role')
        @api.expect(role_model)
        @api.marshal_with(role_model)
        def put(self, role_id):
            """Update a role given its identifier"""
            role = Roles.query.get_or_404(role_id)
            data = api.payload
            if data.get('role_name'):
                role.role_name = data['role_name']
            db.session.commit()
            return role

        @api.doc('delete_role')
        @api.response(204, 'Role deleted')
        def delete(self, role_id):
            """Delete a role given its identifier"""
            role = Roles.query.get_or_404(role_id)
            db.session.delete(role)
            db.session.commit()
            return '', 204

    return api
