from flask import jsonify, request, Flask
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy import event

from app import db
from app.models.asn import ASN

##########
### DB ###
##########

## database model representing prefixes
class Prefix(db.Model):
    ## metadata
    __tablename__ = 'prefix'

    ## columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    asn = db.Column(db.Integer, db.ForeignKey('asn.asn', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    cidr = db.Column(db.String(100), unique=True, nullable=False)  ##ASSUMPTION: unique

###########
### API ###
###########

## API Fieldds
prefix_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'asn': fields.Integer,
    'cidr': fields.String
}

## Get all prefixes or create/update a prefix based on data in a json payload
class PrefixRoot(Resource):

    @marshal_with(prefix_fields)
    def get(self):
        prefixes = Prefix.query.all()
        return prefixes, 200
    
    ## CREATE SINGLE PREFIX
    @marshal_with(prefix_fields)
    def post(self):
        args = request.get_json()
        prefix = False
        prefix = db.session.query(Prefix).filter(Prefix.cidr == args.get('cidr')).first()

        if not prefix:
            new_prefix = Prefix(cidr=args.get('cidr'), asn=args.get('asn'), name=args.get('name'))
            db.session.add(new_prefix)
            db.session.commit()
            
            prefix = db.session.query(Prefix).filter(Prefix.cidr == args.get('cidr')).first()
            return prefix, 201
        else:
            return {'error': 'Prefix already exists'}, 409
    
    ## UPDATE
    @marshal_with(prefix_fields)
    def put(self):
        args = request.get_json()
        prefix = db.session.get(Prefix, args.get('id'))
        
        if args.get('asn', False):
            if not db.session.get(ASN, args.get('asn')):
                return {'error': 'IntegrityError: asn({}) was not found'.format(args.get('asn', prefix.asn))}, 409

        if prefix:
            prefix.id = args.get('id', prefix.id)
            prefix.asn = args.get('asn', prefix.asn)
            prefix.name = args.get('name', prefix.name)
            prefix.cidr = args.get('cidr', prefix.cidr)
            db.session.commit()
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404

## Interact with a prefix based on its ID
class PrefixById(Resource):
    
    ## GET
    @marshal_with(prefix_fields)
    def get(self, id):
        prefix = db.session.get(Prefix, id)
        if prefix:
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404

    ## UPDATE
    @marshal_with(prefix_fields)
    def put(self, id):
        args = request.get_json()
        prefix = db.session.get(Prefix,id)
        
        if args.get('asn', False):
            if not db.session.get(ASN, args.get('asn')):
                return {'error': 'IntegrityError: asn({}) was not found'.format(args.get('asn', prefix.asn))}, 409

        if prefix:
            prefix.id = args.get('id', prefix.id)
            prefix.asn = args.get('asn', prefix.asn)
            prefix.name = args.get('name', prefix.name)
            prefix.cidr = args.get('cidr', prefix.cidr)
            db.session.commit()
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404


    ## DELETE
    def delete(self, id):
        prefix = db.session.get(Prefix,id)
        if prefix:
            db.session.delete(prefix)
            db.session.commit()
            return {'message': 'Prefix deleted succesfully'}, 200
        else:
            return {'error': 'Prefix not found'}, 404
