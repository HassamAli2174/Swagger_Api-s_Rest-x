from flask import Flask
from flask_cors import CORS
from extensions import db, api, migrate, jwt
from config import Config
from routes.auth_routes import create_auth_namespace
from routes.crud_user import create_crud_user_namespace
from routes.company_route import create_crud_company_namespace
from routes.roles_route import create_roles_namespace
from routes.courses_route import create_courses_namespace
from routes.student_routes import create_students_namespace
from routes.enrollment import create_enrollment_namespace


app = Flask(__name__)

app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow CORS for specific routes
db.init_app(app)  # Initialize SQLAlchemy
migrate.init_app(app, db)  # Initialize Flask-Migrate f
jwt.init_app(app)

# Configure Swagger UI
# Bearer Token Authorization
api.authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add a JWT with **Bearer <JWT>** to authorize",
    }
}
api.title = "API"
api.description = "Api's for User Management System"
api.version = "1.0"
api.security = "Bearer Auth"

api.init_app(app)  # Initialize Flask-RESTx with the app

# Add API namespaces
api.add_namespace(create_auth_namespace(), path="/api/v1/auth")
api.add_namespace(create_crud_user_namespace(), path="/api/v1/users")
api.add_namespace(create_crud_company_namespace(), path="/api/v1/company")
api.add_namespace(create_roles_namespace(), path="/api/v1/roles")
api.add_namespace(create_courses_namespace(), path="/api/v1/courses")
api.add_namespace(create_students_namespace(), path="/api/v1/students")
api.add_namespace(create_enrollment_namespace(), path="/api/v1/enrollments")

# Run the application
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
