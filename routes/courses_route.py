from extensions import db
from models.course import Course
from flask_restx import Namespace, Resource, fields


def create_courses_namespace():
    api = Namespace('Course', description='Course operations')
    
    course_model = api.model('Course', {
        'course_id': fields.Integer(description='Course ID'),
        'course_name': fields.String(required = True , description='Course Name')
    })
    
    class CourseResource(Resource):
        @api.marshal_list_with(course_model)
        def get(self):
            """Get all courses"""
            courses = Course.query.all()
            return courses
        
        @api.expect(course_model)
        def post(self):
            data = api.payload
            course = Course(course_name=data['course_name'])
            db.session.add(course)
            db.session.commit()
            return {'success': 'Course added'}, 201

    api.add_resource(CourseResource, '/')
    return api