from extensions import db

class Student(db.Model):
    __tablename__ = 'student'
    std_id = db.Column(db.Integer, primary_key=True)
    std_name = db.Column(db.String(255), nullable=False)
    enrollments = db.relationship('Enrollment', back_populates='student')