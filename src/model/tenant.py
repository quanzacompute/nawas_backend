from src.db.connection import DBConnection

from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse

db = DBConnection.get_connection()

class Tenant(db.Model):
    ## metadata
    __tablename__ = 'tenant'

    ## columnm
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ##TODO: add more fields if required

    ## relationships
    asns = db.relationship('ASN', backref='tenant', lazy=True)


tenant_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'asns': fields.List(fields.Nested({
        'asn': fields.Integer,
        'prefixes': fields.List(fields.Nested({
            'id': fields.Integer,
            'cidr': fields.String
        }))
    }))    
}

## retrieve a list of all tenants
class TenantList(Resource):
    @marshal_with(tenant_fields)
    def get(self):
        tenants = Tenant.query.all()
        return tenants, 200

## get, update or delete tenants based of id
class TenantById(Resource):
    ## GET
    @marshal_with(tenant_fields, envelope='resource')
    def get(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        if tenant:
            return tenant, 200
        else:
            return {'error': 'Tenant not found'}, 404

    ## UPDATE
    @marshal_with(tenant_fields, envelope='resource')
    def put(self, tenant_id):
        args = request.get_json()
        tenant = Tenant.query.get(tenant_id)

        if tenant:
            tenant.id = args.get('id', tenant.id)
            tenant.name = args.get('name', tenant.name)
            db.session.commit()
            return tenant, 200
        else:
            return {'error', 'Tenant not found'}, 404
            

    ## DELETE
    def delete(self, tenant_id):
        tenant = Tenant.query.get(tenant_id)
        
        if tenant:
            db.session.delete(tenant)
            db.session.commit()
            return {'message': 'Tenant deleted successfully'}, 200
        else:
            return {'error', 'Tenant not found'}, 404

## get or add tenants based of name
def TenantByName(Resource):
    ## GET
    @marshal_with(tenant_fields)
    def get(self, tenant_name):
        tenant = Tenant.query.get(name=tenant_name).first()
        if tenant:
            return tenant, 200
        else:
            return {'error': 'Tenant not found'}, 404
    
    ## CREATE
    @marshal_with(tenant_fields)
    def post(self, tenant_name):
        args = request.get_json()
        tenant = Tenant.query.filter_by(name=tenant_name).first()
        if tenant:
            return {'error': 'Tenant already exists'}, 409
        else:
            # Creating a new tenant
            new_tenant = Tenant(name=tenant_name)
            db.session.add(new_tenant)
            db.session.commit()
            return new_tenant, 201
    

    
