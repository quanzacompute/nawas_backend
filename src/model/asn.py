from src.db.connection import DBConnection

from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse

from src.model.tenant import Tenant


db = DBConnection.get_connection()

class ASN(db.model):
    ## metadata
    __tablename__ = 'asn'

    ## column
    asn = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    tenant = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False, onupdate="CASCADE", ondelete="RESTRICT")

    # relationships
    refixes = db.relationship('Prefix', backref='asn', lazy=true)

asn_fields = {
    'asn': fields.Integer,
    'tenant_id': fields.Integer
    'prefixes': fields.List(fields.Nested({
        'id': fields.Integer,
        'cidr': fields.String
    }))
}

## retrieve a list of all asns
class ASNList(Resource):
    @marshal_with(asn_fields)
    def get(self):
        asns = ASN.query.all()
        return asns, 200

        
class ASNbyASN(Resource):
    
    ## GET
    @marshal_with(asn_fields)
    def get(self, asn):
        asn = ASN.query.get(asn)
        if asn:
            return asn, 200
        else:
            return {'error': 'ASN not found'}, 404

    ## UPDATE
    @marshal_with(asn_fields)
    def put(self, asn):
        args = request.get_json()
        asn = ASN.query.get(asn)

        if asn:
            asn.id = args.get('id', asn.id)
            ans.tenant_id = args.get('tenant_id', asn.tenant_id)
            db.session.commit()
            return asn, 200
        else:
            return {'error': 'ASN not found'}, 404

    ## CREATE
    @marshal_with(asn_fields)
    def post(self, asn):
        asn = ASN.query.get(asn)
        
        if not asn:
            asn.id = args.get('id', asn.id)
            ans.tenant_id = args.get('tenant_id', asn.tenant_id)
            db.session.commit()
            return asn, 201
        else:
            return {'error': 'ASN already exists'}, 409

    ## DELETE
    def delete(self, asn):
        asn = ASN.query.get(asn)
        if asn:
            db.session.delete(asn)
            db.session.commit()
        else:
            return {'error': 'ASN not found'}, 404



    

