
from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse

from app import db

##########
### DB ###
##########


class ASN(db.Model):
    ## metadata
    __tablename__ = 'asn'

    ## column
    asn = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

    # relationships
    refixes = db.relationship('Prefix', backref='asn_relationship', lazy=True)

###########
### API ###
###########


asn_fields = {
    'asn': fields.Integer,
    'tenant_id': fields.Integer,
    'prefixes': fields.List(fields.Nested({
        'id': fields.Integer,
        'cidr': fields.String
    }))
}

## retrieve a list of all asns
class ASNRoot(Resource):
    @marshal_with(asn_fields)
    def get(self):
        asns = ASN.query.all()
        return asns, 200

        
class ASNByASN(Resource):
    
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
            asn.asn = args.get('asn', asn.asn)
            asn.tenant_id = args.get('tenant_id', asn.tenant_id)

            db.session.commit()
            return asn, 200
        else:
            return {'error': 'ASN not found'}, 404

    ## CREATE
    @marshal_with(asn_fields)
    def post(self, asn):
        args = request.get_json()
        asnObj = ASN.query.get(asn)
        if args.get('tenant_id', None) is None:
            return {'error': 'Please provide a tenant_id to create an ASN'}, 400


        if not asnObj:
            new_asn = ASN(
                asn = args.get('asn', asn),
                tenant_id = args.get('tenant_id')
            )

            db.session.add(new_asn)
            db.session.commit()
            return new_asn, 201
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



    

