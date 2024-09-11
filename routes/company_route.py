# routes/crud_company.py
from flask_restx import Namespace, Resource, fields
from models.company import Company
from extensions import db


def create_crud_company_namespace():
    api = Namespace("Company_CRUD", description="Company CRUD operations")
    company_model = api.model(
        "Company",
        {
            "company_id": fields.Integer(
                readOnly=True, description="The unique identifier of a company"
            ),
            "company_name": fields.String(required=True, description="Company name"),
            "company_email": fields.String(required=True, description="Company email"),
            "company_desc": fields.String(
                required=True, description="Company description"
            ),
            "company_register_number": fields.String(
                required=True, description="Company registration number"
            ),
        },
    )

    @api.route("/")
    class CompanyList(Resource):
        def get(self):
            """Retrieve all companies"""
            companies = Company.query.all()
            return api.marshal(companies, company_model), 200

        @api.expect(company_model)
        def post(self):
            """Create a new company"""
            data = api.payload
            company = Company(
                company_name=data["company_name"],
                company_email=data["company_email"],
                company_desc=data["company_desc"],
                company_register_number=data["company_register_number"],
            )
            db.session.add(company)
            db.session.commit()
            return {"message": "Company created successfully"}, 201

    @api.route("/<int:company_id>")
    @api.response(404, "Company not found")
    @api.param("company_id", "The company identifier")
    class CompanyResource(Resource):
        def get(self, company_id):
            """Retrieve a company by its ID"""
            company = Company.query.get_or_404(company_id)
            return api.marshal(company, company_model), 200

        @api.expect(company_model)
        def put(self, company_id):
            """Update a company given its identifier"""
            company = Company.query.get_or_404(company_id)
            data = api.payload
            for key, value in data.items():
                setattr(company, key, value)
            db.session.commit()
            return {"message": "Company updated successfully"}, 200

        def delete(self, company_id):
            """Delete a company given its identifier"""
            company = Company.query.get_or_404(company_id)
            db.session.delete(company)
            db.session.commit()
            return {"message": "Company deleted successfully"}, 204

    return api
