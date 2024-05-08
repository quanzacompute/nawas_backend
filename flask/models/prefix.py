from flask import jsonify, request, Flask
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy import event

from app import app,db

##########
### DB ###
##########

class Prefix(db.Model):
    ## metadata
    __tablename__ = 'prefix'

    ## columns
    id = db.Column(db.Integer, primary_key=True)
    asn = db.Column(db.Integer, db.ForeignKey('asn.asn', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    cidr = db.Column(db.String(100), unique=True, nullable=False)  ##ASSUMPTION: unique

###########
### API ###
###########

prefix_fields = {
    'id': fields.Integer,
    'asn': fields.Integer,
    'cidr': fields.String
}

class PrefixRoot(Resource):

    @marshal_with(prefix_fields)
    def get(self):
        prefixes = Prefix.query.all()
        return prefixes, 200
    
    ## CREATE SINGLE PREFIX
    @marshal_with(prefix_fields)
    def post(self):
        args = request.get_json()
        prefix = Prefix.query.filter_by(cidr=args.get('cidr')).first()
        if not prefix:
            new_prefix = Prefix(cidr=args.get('cidr'), asn=args.get('asn'))
            db.session.add(new_prefix)
            db.session.commit()
            
            prefix = Prefix.query.filter_by(cidr=args.get('cidr')).first()
            return prefix, 201
        else:
            return {'error': 'Prefix already exists'}, 409
    
    ## UPDATE
    @marshal_with(prefix_fields)
    def put(self):
        args = request.get_json()
        prefix = Prefix.query.get(args.get('id'))
        if prefix:
            prefix.id = args.get('id', prefix.id)
            prefix.asn = args.get('asn', prefix.asn)
            prefix.cidr = args.get('cidr', prefix.cidr)
            db.session.commit()
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404

class PrefixById(Resource):
    
    ## GET
    @marshal_with(prefix_fields)
    def get(self, id):
        prefix = Prefix.query.get(id)
        if prefix:
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404

    ## UPDATE
    @marshal_with(prefix_fields)
    def put(self, id):
        args = request.get_json()
        prefix = Prefix.query.get(id)
        if prefix:
            prefix.id = args.get('id', prefix.id)
            prefix.asn = args.get('asn', prefix.asn)
            prefix.cidr = args.get('cidr', prefix.cidr)
            db.session.commit()
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404


    ## DELETE
    def delete(self, id):
        prefix = Prefix.query.get(id)
        if prefix:
            db.session.delete(prefix)
            db.session.commit()
            return {'message': 'Prefix deleted succesfully'}, 200
        else:
            return {'error': 'Prefix not found'}, 404
