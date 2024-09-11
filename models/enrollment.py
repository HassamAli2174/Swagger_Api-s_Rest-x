from extensions import db

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    std_id = db.Column(db.Integer, db.ForeignKey('student.std_id'))
    course = db.relationship('Course', back_populates='enrollments')
    student = db.relationship('Student', back_populates='enrollments')