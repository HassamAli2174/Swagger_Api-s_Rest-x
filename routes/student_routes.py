# routes/crud_student.py
from flask_restx import Namespace, Resource, fields
from models.student import Student
from extensions import db


def create_students_namespace():
    api = Namespace('Student', description='Student operations')

    student_model = api.model('Student', {
        'std_id': fields.Integer(description='Student ID'),
        'std_name': fields.String(required=True, description='Student name'),
    })

    class StudentResource(Resource):
        @api.marshal_list_with(student_model)
        def get(self):
            students = Student.query.all()
            return students

        @api.expect(student_model)
        def post(self):
            data = api.payload
            student = Student(std_name=data['std_name'])
            db.session.add(student)
            db.session.commit()
            return {'success': 'Student added'}, 201

    api.add_resource(StudentResource, '/')
    return api