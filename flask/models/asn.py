
from sqlalchemy.exc import IntegrityError
from flask import jsonify, request, current_app
from flask_restful import Resource, fields, marshal_with, reqparse

from app import db
from app.models.tenant import Tenant 

##########
### DB ###
##########

## Database model representing the ASN object
class ASN(db.Model):
    ## metadata
    __tablename__ = 'asn'

    ## column
    asn = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    name = db.Column(db.String, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

    # relationships
    prefixes = db.relationship('Prefix', backref='asn_relationship', lazy=True)

###########
### API ###
###########

## api fields for ASN
asn_fields = {
    'asn': fields.Integer,
    'name': fields.String,
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

## interact with sinle ASN based on unique asn field
class ASNByASN(Resource):
    
    ## GET
    @marshal_with(asn_fields)
    def get(self, asn):
        asn = db.session.get(ASN, asn)
        if asn:
            return asn, 200
        else:
            return {'error': 'ASN not found'}, 404

    ## UPDATE
    @marshal_with(asn_fields)
    def put(self, asn):
        args = request.get_json()
        asn = db.session.get(ASN, asn)

        if asn:
            asn.asn = args.get('asn', asn.asn)
            asn.name = args.get('name', asn.name)
            asn.tenant_id = args.get('tenant_id', asn.tenant_id)

            if not db.session.get(Tenant, asn.tenant_id):
                return {'error': 'IntegrityError: tenant_id({}) was not found'.format(asn.tenant_id)}, 409

            db.session.commit()
            return asn, 200
        else:
            return {'error': 'ASN not found'}, 404

    ## CREATE
    @marshal_with(asn_fields)
    def post(self, asn):
        args = request.get_json()
        asnObj = db.session.get(ASN, asn)
        if args.get('tenant_id', None) is None:
            return {'error': 'Please provide a tenant_id to create an ASN'}, 400


        if not asnObj:
            new_asn = ASN(
                asn = args.get('asn', asn),
                name = args.get('name'),
                tenant_id = args.get('tenant_id')
            )

            db.session.add(new_asn)
            db.session.commit()
            return new_asn, 201
        else:
            return {'error': 'ASN already exists'}, 409

    ## DELETE
    def delete(self, asn):
        asn = db.session.get(ASN, asn)
        if asn:
            try :
                db.session.delete(asn)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                return {'error': str(e) }, 409
        else:
            return {'error': 'ASN not found'}, 404



    

