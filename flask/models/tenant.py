
from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse

from app import db

##########
### DB ###
##########

## database model representing a tenant object
class Tenant(db.Model):
    ## metadata
    __tablename__ = 'tenant'

    ## columnm
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ##TODO: add more fields if required

    ## relationships
    asns = db.relationship('ASN', backref='tenant_relationship', lazy=True)

##########
### API ###
##########

## api fields
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
class TenantRoot(Resource):
    @marshal_with(tenant_fields)
    def get(self):
        tenants = Tenant.query.all()
        return tenants, 200
    
    ## CREATE
    @marshal_with(tenant_fields)
    def post(self):
        args = request.get_json()
        name = args.get('name', None)
        if name is None:
            return {'error': 'No Tenant Name Received'}, 400

        tenant = db.session.query(Tenant).filter(Tenant.name == name).first()
        if tenant:
            return {'error': 'Tenant already exists'}, 409
        else:
            # Creating a new tenant
            new_tenant = Tenant(name=name)
            db.session.add(new_tenant)
            db.session.commit()

            ## retrieve added tenant
            tenant = db.session.query(Tenant).filter(Tenant.name == new_tenant.name).first()
            return tenant, 201

## get, update or delete tenants based of id
class TenantById(Resource):
    ## GET
    @marshal_with(tenant_fields, envelope='resource')
    def get(self, id):
        tenant = db.session.get(Tenant,id)
        if tenant:
            return tenant, 200
        else:
            return {'error': 'Tenant not found'}, 404

    ## UPDATE
    @marshal_with(tenant_fields, envelope='resource')
    def put(self, id):
        args = request.get_json()
        tenant = db.session.get(Tenant,id)

        if tenant:
            tenant.id = args.get('id', tenant.id)
            tenant.name = args.get('name', tenant.name)
            db.session.commit()
            return tenant, 200
        else:
            return {'error', 'Tenant not found'}, 404
    
    ## DELETE
    def delete(self, id):
        tenant = db.session.get(Tenant,id)
        
        if tenant:
            db.session.delete(tenant)
            db.session.commit()
            return {'message': 'Tenant deleted successfully'}, 200
        else:
            return {'error', 'Tenant not found'}, 404

## get or add tenants based of name
class TenantByName(Resource):
    ## GET
    @marshal_with(tenant_fields)
    def get(self, name):
        tenant = db.session.query(Tenant).filter(Tenant.name == name).first()
        if tenant:
            return tenant, 200
        else:
            return {'error': 'Tenant not found'}, 404
    
    ## CREATE
    @marshal_with(tenant_fields)
    def post(self, name):
        args = request.get_json()
        tenant = db.session.query(Tenant).filter(Tenant.name == name).first()
        if tenant:
            return {'error': 'Tenant already exists'}, 409
        else:
            # Creating a new tenant
            new_tenant = Tenant(name=name)
            db.session.add(new_tenant)
            db.session.commit()

            ## retrieve added tenant
            tenant = db.session.query(Tenant).filter(Tenant.name == new_tenant.name).first()
            return tenant, 201
    

    
