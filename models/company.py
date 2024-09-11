from extensions import db


class Company(db.Model):
    __tablename__ = 'company'
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_email = db.Column(db.String(255), nullable=False)
    company_desc = db.Column(db.String(255), nullable=False)
    company_register_number = db.Column(db.String(255), nullable=False)