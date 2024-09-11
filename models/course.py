from extensions import db


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    enrollments = db.relationship('Enrollment', back_populates='course')