# routes/crud_enrollment.py
from flask_restx import Namespace, Resource, fields
from models.enrollment import Enrollment
from extensions import db

def create_enrollment_namespace():
    api = Namespace('Enrollment', description='Enrollment operations')

    enrollment_model = api.model('Enrollment', {
        'enrollment_id': fields.Integer(description='Enrollment ID'),
        'course_id': fields.Integer(required=True, description='Course ID'),
        'std_id': fields.Integer(required=True, description='Student ID'),
    })

    class EnrollmentResource(Resource):
        @api.marshal_list_with(enrollment_model)
        def get(self):
            enrollments = Enrollment.query.all()
            return enrollments

        @api.expect(enrollment_model)
        def post(self):
            data = api.payload
            enrollment = Enrollment(course_id=data['course_id'], std_id=data['std_id'])
            db.session.add(enrollment)
            db.session.commit()
            return {'success': 'Enrollment added'}, 201

    api.add_resource(EnrollmentResource, '/')
    return api